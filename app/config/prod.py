#! python3
# -*- encoding: utf-8 -*-

import os
from .base import Config


class ProdConfig(Config):
    # sqlalchemy mysql
    USERNAME = os.getenv('DB_USERNAME', 'username')
    PASSWORD = os.getenv('DB_PASSWORD', 'password')
    HOST = os.getenv('DB_HOST', 'xxx.xxx.xxx.xxx')
    PORT = int(os.getenv('DB_PORT', 3306))
    DATABASE = os.getenv('DB_NAME', 'flask_demo')

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'. \
        format(USERNAME, PASSWORD, HOST, PORT, DATABASE)

    # flask-apscheduler 存储的位置,用于定时任务的持久化
    # SCHEDULER_JOBSTORES = {
    #     'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
    # }