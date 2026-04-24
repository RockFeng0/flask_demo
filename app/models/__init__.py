#! python3
# -*- encoding: utf-8 -*-

from .base import BaseModel
from .department import DepartmentModel
from .staff import StaffModel
from .user import User

__all__ = ["BaseModel", "DepartmentModel", "StaffModel", "User"]
