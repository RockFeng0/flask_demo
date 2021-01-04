#! python3
# -*- encoding: utf-8 -*-


from flask import Blueprint
from flask_restful import Api
from app.src.resources.department import DepartmentListView, DepartmentView
from app.src.resources.staff import StaffListView, StaffView

organization = Blueprint('organization', __name__)
api = Api(organization)
api.add_resource(DepartmentListView, '/department')
api.add_resource(DepartmentView, '/department/<int:id>')
api.add_resource(StaffListView, '/staff')
api.add_resource(StaffView, '/staff/<int:id>')
