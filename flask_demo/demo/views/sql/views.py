#! python3
# -*- encoding: utf-8 -*-
'''
Current module: demo.views.sql.views

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      demo.views.sql.views,v 1.0 2019年2月20日
    FROM:   2019年2月20日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import datetime
from flask import request, jsonify
from flask.views import MethodView

from flask_demo.demo.views.sql import sql
from flask_demo.demo.views.sql.models import DbDemo, db

def get_query():
    return db.session.query(DbDemo)

def get_result(result, status=True, message="" ):
    return {"status":status, "message":message,"result":result}


class UsageSqlalchemyViews(MethodView):
    
    def get(self):
        # GET /demo
        param = dict(request.args.items())        
        _query = get_query()
                     
        conditions = {i: param.get(i) for i in ('id', 'name') if param.get(i)}        
        base_conditions = _query.filter_by(**conditions).order_by(DbDemo.update_time.desc())
                
        page = int(param.get("page", 1))
        size = int(param.get("size", 10))
        pagination = base_conditions.paginate(page = page, per_page= size, error_out=False)
        
        result = {"total": pagination.total, "demos":[]}        
        for demo in pagination.items:
            _demo = {}
            _demo['id'] = demo.id
            _demo['name'] = demo.name
            _demo['desc'] = demo.desc
            _demo["create_time"] = demo.create_time.strftime("%Y-%m-%d %H:%M:%S")
            _demo["update_time"] = demo.update_time.strftime("%Y-%m-%d %H:%M:%S")
            
            result["demos"].append(_demo)
                
        return jsonify(get_result(result, message = "get all demos success in page: {0} size: {1}.".format(page, size)))
    
    def post(self):
        # POST /demo        
        j_param = request.json if request.data else request.form.to_dict()
        _query = get_query()       
        now = datetime.datetime.now()
        
        try:
            
            for param in ("name", ):
                _param = j_param.get(param)
                if not _param:
                    return jsonify(get_result("", status = False, message = 'Demo parameter [{0}] should not be null.'.format(param)))
            
            data = _query.filter_by(name = j_param.get("name")).first()
                        
            if data:
                status = False
                message = "this demo is already exists."                            
            else:                
                _case = DbDemo(j_param.get("name"), j_param.get("desc",""),now, now)                
                db.session.add(_case)                
                db.session.flush()
                db.session.commit()
                
                status = True              
                message = "add demo success."
        except Exception as e:
            message = str(e)
            status = False
        return jsonify(get_result("", status = status, message = message))
    
    def put(self):
        # PUT /demo?demo_id=32342
        param = dict(request.args.items())
        j_param = request.json if request.data else request.form.to_dict()
        _query = get_query()                
        now = datetime.datetime.now()
        
        try: 
            data = _query.filter_by(id = param.get("demo_id")).first()
                                    
            if not data:
                message = "do not have the demo with demo_id({})".format(param.get("demo_id"))
                return jsonify(get_result("", status = False, message = message))
            
            for pp in ("name", ):
                _param = j_param.get(pp)
                if not _param:
                    return jsonify(get_result("", status = False, message = 'Demo parameter [{0}] should not be null.'.format(pp)))                
                
            for i in ["name", "desc"]:
                setattr(data, i, j_param.get(i,""))            
            data.update_time = now
            db.session.flush()
            db.session.commit()
            
            status = True
            message = "update demo success."         
        except Exception as e:
            message = str(e)
            status = False
    
        return jsonify(get_result("", status = status, message = message))       
    
    def delete(self):
        # DELETE /demo?demo_id=32342
        param = dict(request.args.items())
        _query = get_query()
        
        data = _query.filter_by(id = param.get("demo_id")).first()
        
        if data:
            db.session.delete(data)                            
            db.session.commit()
            
            status = True
            message = "delete demo success."        
        else:
            status = False
            message = "do not have the demo with demo_id({})".format(param.get("demo_id"))
        return jsonify(get_result("", status = status,message = message))

    
sql.add_url_rule('/demo', view_func=UsageSqlalchemyViews.as_view('db_demo'))

