#! python3
# -*- encoding: utf-8 -*-

from app.config import db, bcrypt
from app.models.base import BaseModel
from itsdangerous import URLSafeSerializer
from flask import current_app


class User(db.Model, BaseModel):
    """
    用户表
    """

    __tablename__ = "user_info"

    email = db.Column(db.String(255), unique=True, nullable=False, index=True, comment="邮箱")
    mobile_number = db.Column(
        db.String(20), unique=True, nullable=False, index=True, comment="手机号"
    )
    username = db.Column(db.String(50), nullable=False, index=True, comment="用户名")
    password = db.Column(db.String(255), nullable=False, comment="密码")
    about_me = db.Column(db.String(255), nullable=True, comment="关于我")
    is_active = db.Column(db.Boolean, default=True, comment="是否激活")

    def set_password(self, password):
        """
        设置密码
        """
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        """
        检查密码
        """
        return bcrypt.check_password_hash(self.password, password)

    def get_id(self, life_time=None):
        """
        获取用户id
        """
        if life_time is None:
            # Flask-Login调用时使用默认值
            return str(self.id)
        key = current_app.config.get("SECRET_KEY")
        s = URLSafeSerializer(key)
        return s.dumps([self.id, self.username, self.password, life_time])
