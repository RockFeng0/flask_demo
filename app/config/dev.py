#! python3
# -*- encoding: utf-8 -*-

import os
from .base import Config, ROOT_PATH
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


class DevConfig(Config):
    DEBUG = True
    _sqlite_db_path = os.path.join(ROOT_PATH, "flask_demo.db")
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(_sqlite_db_path)

    # flask-apscheduler 存储的位置,用于定时任务的持久化
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
    }

    # 需要绑定的多个数据库:  __bind_key__ = 'auto'
    # USERNAME = "username"
    # PASSWORD = "password"
    # HOST = "xxx.xxx.xxx.xxx"
    # PORT = 3306
    # DATABASE = 'flask_demo'
    #
    # SQLALCHEMY_BINDS = {
    #     'auto': 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOST, PORT, DATABASE),
    # }