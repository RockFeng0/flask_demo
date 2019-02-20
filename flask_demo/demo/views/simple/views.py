#! python3
# -*- encoding: utf-8 -*-
'''
Current module: demo.views.simple.views

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      demo.views.simple.views,v 1.0 2019年2月20日
    FROM:   2019年2月20日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

from flask import request, jsonify
from flask_demo.demo.views.simple import simple


_msg = {"status":"ok", "result":"", "msg":""}

@simple.route('add', methods=["GET"])
def add_get():
    # GET /add?x=1&y=2
    param = dict(request.args.items())
    
    try:
        _msg["result"] = int(param.get('x')) + int(param.get('y'))        
    except Exception as e:
        _msg["status"] = "error"
        _msg["msg"] = str(e)
    return jsonify(_msg)

@simple.route('add', methods=["POST"])
def add_post():
    # POST /add        
    j_param = request.json if request.data else request.form.to_dict()        
    
    try:
        _msg["result"] = int(j_param.get('x')) + int(j_param.get('y'))        
    except Exception as e:
        _msg["status"] = "error"
        _msg["msg"] = str(e)
    return jsonify(_msg)
