#! python3
# -*- encoding: utf-8 -*-
'''
Current module: demo.views.views

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      demo.views.views,v 1.0 2019年2月20日
    FROM:   2019年2月20日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

from flask_demo.demo import app

@app.route('/', methods=["GET"])
def index():
    return 'flask demo is ready.'