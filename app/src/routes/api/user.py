#! python3
# -*- encoding: utf-8 -*-
# 用户视图

from flask import Blueprint
from flask import jsonify, current_app, abort
from flask_restful.reqparse import RequestParser
from flask_login import login_user, logout_user, login_required

from sqlalchemy.exc import SQLAlchemyError
from itsdangerous import URLSafeSerializer, BadData

from app.com import code
from app.com.pretty import pretty_result
from app.config import db, login_manager, simple_cache
from app.src.models.user_info import User


user = Blueprint('user', __name__)
@login_manager.user_loader
def load_user(token):
    key = current_app.config.get("SECRET_KEY")
    try:
        s = URLSafeSerializer(key)
        userid, username, password, life_time = s.loads(token)
    except BadData:
        # token had been modified!
        return None

    # 校验密码
    _user = db.session.query(User).get(userid)

    if _user:
        # 能loads出id，name等信息，说明已经成功登录过，那么cache中就应该有token的缓存
        token_cache = simple_cache.get(token)

        # 此处找不到有2个原因：
        # 1.cache中因为超时失效（属于正常情况）；
        # 2.cache机制出错（属于异常情况）。
        if not token_cache:
            # the token is not found in cache.
            return None

        # 校验password-hash是否一致
        if str(password) != str(_user.password):
            # the password in token is not matched!
            simple_cache.delete(token)
            return None
        else:
            simple_cache.set(token, 1, timeout=life_time)
    else:
        # the user is not found, the token is invalid!
        return None
    return _user


class UserAuth(object):

    @staticmethod
    @user.route("/login", methods=["POST"])
    def login():
        """
            POST /user/login
        """
        parser = RequestParser()
        parser.add_argument("email_or_mobile_number", type=str, location="json", required=True)
        parser.add_argument("password", type=str, location="json", required=True)
        parser.add_argument("remember", type=bool, location="json", default=False)
        args = parser.parse_args()

        try:
            _user = db.session.query(User).filter(db.or_(
                User.email == args.get("email_or_mobile_number"),
                User.mobile_number == args.get("email_or_mobile_number")
            )).first()

        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, '数据库错误！')

        else:
            if not _user:
                return jsonify(pretty_result(code.VALUE_ERROR, msg='未注册的用户.'))

            if _user.check_password(args.get("password")):
                # 密码验证通过，使用login_user函数来登录用户，这时用户在session会话中的状态就是登录状态了
                login_user(_user, remember=args.get("remember"))

                # 设置token缓存, 注意缓存与cookie的区别, cache是存储于服务器的内存, cookie是保存在客户端的一组数据
                life_time = current_app.config.get("TOKEN_LIFETIME")
                token = _user.get_id(life_time)
                simple_cache.set(token, 1, life_time)

                return jsonify(pretty_result(code.OK, data={"token": token, "username": _user.username}))
            else:
                return jsonify(pretty_result(code.AUTHORIZATION_ERROR, msg='密码错误.'))

    @staticmethod
    @user.route("/register", methods=["POST"])
    def register():
        """
            POST /user/register
        """
        parser = RequestParser()
        params = ("email", "mobile_number", "username", "password")
        _ = [parser.add_argument(param, type=str, location="json", required=True) for param in params]
        parser.add_argument("about_me", type=str, location="json")
        args = parser.parse_args()

        try:
            _user = db.session.query(User).filter(db.or_(
                User.email == args.get("email"),
                User.mobile_number == args.get("mobile_number")
            )).first()
            if _user:
                return jsonify(pretty_result(code.PARAM_ERROR, msg='已注册的用户.'))

            _user = User()
            _ = [setattr(_user, param, args.get(param)) for param in params]
            _user.about_me = args.get("about_me")
            db.session.add(_user)
            db.session.flush()
            db.session.commit()
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, '数据库错误！')
        else:
            return jsonify(pretty_result(code.OK))

    @staticmethod
    @user.route("/updater/<int:uid>", methods=["POST"])
    @login_required
    def update_user(uid):
        """
            POST /user/updater/1
        """

        parser = RequestParser()
        params = ("email", "mobile_number", "username", "about_me")
        _ = [parser.add_argument(param, type=str, location="json") for param in params]
        args = parser.parse_args()

        try:
            _user = User.query.get(uid)
            if not _user or _user.is_delete:
                abort(404)

            # email 属性唯一
            if args.get("email") and _user.email != args.get("email") \
                    and db.session.query(User).filter(User.email == args.get("email")).first():
                return jsonify(pretty_result(code.PARAM_ERROR, msg='已存在的用户邮箱.'))

            # mobile_number 属性唯一
            if args.get("mobile_number") and _user.mobile_number != args.get("mobile_number") \
                    and db.session.query(User).filter(User.mobile_number == args.get("mobile_number")).first():
                return jsonify(pretty_result(code.PARAM_ERROR, msg='已存在的用户手机号.'))

            # 属性更新
            _ = [setattr(_user, param, args.get(param)) for param in params if args.get(param)]
            _user.about_me = args.get("about_me")
            db.session.flush()
            db.session.commit()
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, '数据库错误！')
        else:
            return jsonify(pretty_result(code.OK))

    @staticmethod
    @user.route("/logout", methods=["GET"])
    @login_required
    def logout():
        """
            GET /user/logout
        """
        logout_user()
        return jsonify(pretty_result(code.OK))

    @staticmethod
    @user.route('/test')
    @login_required
    def test():
        """
            GET /user/test
        """
        return jsonify(pretty_result(code.OK, msg="test ok."))
