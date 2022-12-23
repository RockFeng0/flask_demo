#! python3
# -*- encoding: utf-8 -*-


from flask import current_app, jsonify, abort
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError

from app.config import db
from app.com import code
from app.com.pretty import pretty_result
from app.src.models.fa_demo_department import DepartmentModel


class DepartmentListView(Resource):

    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        """        GET /organization/department?page=1&size=10
        获取分页的列表，支持参数筛选,参数如下：
            name  -- 部门名称
        """

        _params = ('name',)
        self.parser.add_argument("page_num", type=int, location="args", default=1)
        self.parser.add_argument("page_size", type=int, location="args", default=10)
        _ = [self.parser.add_argument(i, type=str, location="args") for i in _params]
        args = self.parser.parse_args()

        try:
            _base_condition = {
                getattr(DepartmentModel, i).like("%{0}%".format(args.get(i))) for i in _params if args.get(i)
            }

            all_conditions = {DepartmentModel.is_delete == False}.union(_base_condition)
            base_condition = DepartmentModel.query.filter(*all_conditions).order_by(DepartmentModel.update_time.desc())
            pagination = base_condition.paginate(page=args.page_num, per_page=args.page_size, error_out=False)

        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, '数据库错误！')
        else:
            items = [{
                "id": department.id,
                "name": department.name,
                "desc": department.desc,
                "c_time": department.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                "u_time": department.update_time.strftime("%Y-%m-%d %H:%M:%S")
            } for department in pagination.items]

            result = {
                'page_num': args.page_num,
                'page_size': args.page_size,
                "total": base_condition.count(),
                "departments": items
            }
            return jsonify(pretty_result(code.OK, data=result))

    def post(self):
        """        POST /organization/department
        添加数据
            name  -- 部门名称；
            desc -- 描述；
        """

        self.parser.add_argument("name", type=str, location="json", required=True)
        self.parser.add_argument("desc", type=str, location="json")
        args = self.parser.parse_args()

        dept = DepartmentModel.query.filter_by(name=args.get("name")).first()
        if dept:
            return jsonify(pretty_result(code.OK, msg="该部门已存在"))

        try:
            dept = DepartmentModel()
            dept.name = args.get("name")
            dept.desc = args.get("desc")
            db.session.add(dept)
            db.session.flush()
            db.session.commit()

        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, '数据库错误！')
        else:
            return jsonify(pretty_result(code.OK))


class DepartmentView(Resource):

    def __init__(self):
        self.parser = RequestParser()

    @staticmethod
    def get(id):
        """        GET /organization/department/1
        获取数据，参数如下：
            id  -- 数据表的id
        """

        try:
            dept = DepartmentModel.query.get(id)
            if not dept or dept.is_delete:
                abort(404)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, '数据库错误！')
        else:
            result = {
                "id": dept.id,
                "name": dept.name,
                "desc": dept.desc,
                "c_time": dept.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                "u_time": dept.update_time.strftime("%Y-%m-%d %H:%M:%S")
            }

            return jsonify(pretty_result(code.OK, data=result))

    def put(self, id):
        """       PUT /organization/department/1
        更新数据,参数如下：
            id  -- 数据表的id
        """

        self.parser.add_argument("name", type=str, location="json")
        self.parser.add_argument("desc", type=str, location="json")
        args = self.parser.parse_args()

        try:
            dept = DepartmentModel.query.get(id)
            if not dept or dept.is_delete:
                abort(404)
            dept.name = args.name
            dept.desc = args.desc

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
        """       DELETE /organization/department/1
        删除数据,参数如下：
            id  -- 数据表的id
        """
        try:
            dept = DepartmentModel.query.get(id)
            if not dept or dept.is_delete:
                abort(404)

            dept.is_delete = True
            db.session.flush()
            db.session.commit()
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, '数据库错误！')
        else:
            return pretty_result(code.OK)
