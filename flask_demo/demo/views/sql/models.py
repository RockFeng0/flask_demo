#! python3
# -*- encoding: utf-8 -*-
'''
Current module: demo.views.sql.models

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      demo.views.sql.models,v 1.0 2019年2月20日
    FROM:   2019年2月20日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

from flask_demo.demo import db
from sqlalchemy import Column, Integer, String, DateTime
 
class DbDemo(db.Model):
    
    __tablename__ = 'dbdemo'
        
    id              = Column(Integer, primary_key=True)    
    name            = Column(String(32), nullable = False, comment = '名称')
    desc            = Column(String(64), comment = '描述')
        
    create_time     = Column(DateTime, nullable = False)
    update_time     = Column(DateTime, nullable = False)

    def __init__(self, name,desc,create_time,update_time):
        self.name        = name        
        self.desc        = desc
                
        self.create_time = create_time
        self.update_time = update_time    
    
    def __repr__(self):
        return '<DbDemo %r-%r>' % (self.name,self.id)
    