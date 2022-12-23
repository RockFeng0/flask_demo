#! python3
# -*- encoding: utf-8 -*-

from app.config import db
from .base import BaseModel


class StaffModel(db.Model, BaseModel):
    """
    示例职员表
    """
    # __bind_key__ = 'auto'
    __tablename__ = 'fa_demo_staff'

    name = db.Column(db.String(64), nullable=False, comment=u'姓名')
    age = db.Column(db.Integer, nullable=True, comment=u'年龄')
    dep_id = db.Column(db.Integer, nullable=False, comment=u'所属部门的ID')
