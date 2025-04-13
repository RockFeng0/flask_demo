#! python3
# -*- encoding: utf-8 -*-

from flask import Blueprint
from flask_restful import Api
from app.organization_demo.services.department import DepartmentListView, DepartmentView
from app.organization_demo.services.staff import StaffListView, StaffView


bp = Blueprint(name='organization', import_name=__name__, url_prefix="/api/v1.0/organization")

api = Api(bp)
api.add_resource(DepartmentListView, '/department')
api.add_resource(DepartmentView, '/department/<int:id>')
api.add_resource(StaffListView, '/staff')
api.add_resource(StaffView, '/staff/<int:id>')
