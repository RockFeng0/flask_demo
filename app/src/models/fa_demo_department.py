#! python3
# -*- encoding: utf-8 -*-

from app import db
from .base import BaseModel


class DepartmentModel(db.Model, BaseModel):
    """
    示例部门表
    """
    # __bind_key__ = 'auto'
    __tablename__ = 'fa_demo_deparment'

    name = db.Column(db.String(64), unique=True, nullable=False, comment=u'部门名称')
    desc = db.Column(db.String(128), nullable=True, comment=u'部门描述')
