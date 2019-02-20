#! python3
# -*- encoding: utf-8 -*-
'''
Current module: demo.manager

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      demo.manager,v 1.0 2019年2月20日
    FROM:   2019年2月20日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

from flask_demo.demo import app, db
from flask_migrate import Migrate

from flask_demo.demo.views.sql.models import DbDemo

migrate = Migrate(app,db)
