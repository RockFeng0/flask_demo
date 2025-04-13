#! python3
# -*- encoding: utf-8 -*-


from flask import current_app, jsonify, abort
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError

from app.config import db
from com import code
from com.pretty import pretty_result
from app.organization_demo.models.fa_demo_department import DepartmentModel
from app.organization_demo.models.fa_demo_staff import StaffModel


class StaffListView(Resource):

    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        """        GET /organization/staff?page=1&size=10
        获取分页的列表，支持参数筛选,参数如下：
            name  -- 职工名称
        """

        _params = ('name',)
        self.parser.add_argument("page_num", type=int, location="args", default=1)
        self.parser.add_argument("page_size", type=int, location="args", default=10)
        _ = [self.parser.add_argument(i, type=str, location="args") for i in _params]
        args = self.parser.parse_args()

        try:
            _base_condition = {
                getattr(StaffModel, i).like("%{0}%".format(args.get(i))) for i in _params if args.get(i)
            }

            all_conditions = {StaffModel.is_delete == False}.union(_base_condition)
            base_condition = StaffModel.query.filter(*all_conditions).order_by(StaffModel.update_time.desc())
            pagination = base_condition.paginate(page=args.page_num, per_page=args.page_size, error_out=False)

        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, '数据库错误！')
        else:
            items = [{
                "id": staff.id,
                "name": staff.name,
                "desc": staff.age,
                "dep_id": staff.dep_id,
                "c_time": staff.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                "u_time": staff.update_time.strftime("%Y-%m-%d %H:%M:%S")
            } for staff in pagination.items]

            result = {
                'page_num': args.page_num,
                'page_size': args.page_size,
                "total": base_condition.count(),
                "staffs": items
            }
            return jsonify(pretty_result(code.OK, data=result))

    def post(self):
        """        POST /organization/staff
        添加数据
            name  -- 职工姓名
            age -- 职工年龄
            dep_id  -- 所属部门id
        """

        self.parser.add_argument("name", type=str, location="json", required=True)
        self.parser.add_argument("age", type=int, location="json")
        self.parser.add_argument("dep_id", type=int, location="json", required=True)
        args = self.parser.parse_args()

        # 参数校验
        dept = DepartmentModel.query.filter_by(id=args.get("dep_id")).first_or_404("不存在的部门")

        staff = StaffModel.query.filter_by(name=args.get("name")).first()
        if staff:
            return jsonify(pretty_result(code.OK, msg="该职工已存在"))

        try:
            staff = StaffModel()
            staff.name = args.get("name")
            staff.age = args.get("age")
            staff.dep_id = dept.id

            db.session.add(staff)
            db.session.flush()
            db.session.commit()

        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, '数据库错误！')
        else:
            return jsonify(pretty_result(code.OK))


class StaffView(Resource):

    def __init__(self):
        self.parser = RequestParser()

    @staticmethod
    def get(id):
        """        GET /organization/staff/1
        获取数据,参数如下：
            id  -- 数据表的id
        """

        try:
            staff_data = db.session.query(DepartmentModel, StaffModel) \
                .join(StaffModel, StaffModel.dep_id == DepartmentModel.id)\
                .filter(StaffModel.id == id, StaffModel.is_delete == False).first_or_404("数据不存在")
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, '数据库错误！')
        else:
            dept = staff_data.DepartmentModel
            staff = staff_data.StaffModel
            result = {
                "id": staff.id,
                "name": staff.name,
                "desc": staff.age,
                "department": dept.name,
                "c_time": staff.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                "u_time": staff.update_time.strftime("%Y-%m-%d %H:%M:%S")
            }

            return jsonify(pretty_result(code.OK, data=result))

    def put(self, id):
        """       PUT /organization/staff/1
        更新任务记录,参数如下：
            id  -- 数据表的id
        """

        self.parser.add_argument("name", type=str, location="json")
        self.parser.add_argument("age", type=int, location="json")
        self.parser.add_argument("dep_id", type=int, location="json")
        args = self.parser.parse_args()

        try:
            staff = StaffModel.query.get(id)
            if not staff or staff.is_delete:
                abort(404)

            dept = DepartmentModel.query.filter_by(id=args.get("dep_id")).first_or_404("不存在的部门")

            staff.name = args.name
            staff.age = args.age
            staff.dep_id = dept.id

            db.session.flush()
            db.session.commit()
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, '数据库错误！')
        else:
            return jsonify(pretty_result(code.OK))

    @staticmethod
    def delete(id):
        """       DELETE /organization/staff/1
        删除demo,参数如下：
            id  -- 数据表的id
        """
        try:
            staff = StaffModel.query.get(id)
            if not staff or staff.is_delete:
                abort(404)

            staff.is_delete = True
            db.session.flush()
            db.session.commit()
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, '数据库错误！')
        else:
            return pretty_result(code.OK)
