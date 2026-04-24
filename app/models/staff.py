#! python3
# -*- encoding: utf-8 -*-

from app.config import db
from app.models.base import BaseModel


class StaffModel(db.Model, BaseModel):
    """
    示例职工表
    """

    # __bind_key__ = 'auto'
    __tablename__ = "fa_demo_staff"

    name = db.Column(db.String(64), unique=True, nullable=False, index=True, comment="职工姓名")
    age = db.Column(db.Integer, nullable=True, comment="职工年龄")
    dep_id = db.Column(
        db.Integer,
        db.ForeignKey("fa_demo_deparment.id"),
        nullable=False,
        index=True,
        comment="所属部门id",
    )
    dep = db.relationship("DepartmentModel", backref=db.backref("staffs", lazy=True))
