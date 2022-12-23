#! python3
# -*- encoding: utf-8 -*-


from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeSerializer
from app.config import db, bcrypt
from app.src.models.base import BaseModel

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model, BaseModel, UserMixin):
    """
    用户信息表
    """
    __tablename__ = "USRINF"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(24), unique=True, nullable=False)
    mobile_number = db.Column(db.String(18), unique=True, nullable=False)
    username = db.Column(db.String(24), unique=False, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    def get_id(self, life_time=None):
        """ @override UserMixin.get_id
        在对应的user id时，可以使用uuid.uuid4()生成一个用户唯一id，这里使用URLSafeSerializer生成token
        :param life_time: 设置session生命周期
        :return:
        """
        key = current_app.config.get("SECRET_KEY")
        s = URLSafeSerializer(key)
        if not life_time:
            life_time = current_app.config.get("TOKEN_LIFETIME")
        # set token with password-hash
        token = s.dumps((self.id, self.username, str(self.password), life_time))
        return token

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

