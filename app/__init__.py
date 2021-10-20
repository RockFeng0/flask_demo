#! python3
# -*- encoding: utf-8 -*-

import re
import logging
import importlib

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

# from flask_login import LoginManager
# from flask_bcrypt import Bcrypt

from utils import log
from app import pretty
from app.config import APP_ENV, configs

# 获取日志对象
logger = logging.getLogger(__name__)
logger.addHandler(log.console)
logger.addHandler(log.log_handler)
logger.addHandler(log.err_handler)
logger.setLevel(logging.DEBUG)


# 创建跨域对象： 解决跨域问题
cors = CORS()

# 创建数据库对象： 处理数据库对象关系映射
db = SQLAlchemy()

# 创建计划任务对象： 处理定时任务
scheduler = APScheduler()

# 创建登录管理对象： 处理用户登录
# login_manager = LoginManager()

# 创建加密对象： 处理用户登录密码
# bcrypt = Bcrypt()

# 创建一个缓存对象
# simple_cache = SimpleCache()


def create_app():
    """
    创建app
    """
    app = Flask(__name__)
    configuration = configs[APP_ENV]

    # 将配置读取到flask对象中
    app.config.from_object(configuration)

    # 对象的初始化
    configuration.init_app(app)
    db.init_app(app)
    cors.init_app(app, supports_credentials=True)
    scheduler.init_app(app)
    scheduler.start()
    # login_manager.init_app(app)
    # bcrypt.init_app(app)

    # 处理蓝图
    blue_prints = app.config.get("ALL_BLUE_PRINT")
    prefix_endpoint = app.config.get("PREFIX_ENDPOINT")
    for suffix_endpoint, blue_print_attr in blue_prints.items():
        # 开关是关闭的就跳过
        if blue_print_attr.get("is_off"):
            continue

        # noinspection PyBroadException
        try:
            # 生成url前缀
            _end_point = "{0}.{1}".format(prefix_endpoint, suffix_endpoint)
            obj = importlib.import_module(_end_point)

            # 定义蓝图名称
            name = blue_print_attr.get("name") if blue_print_attr.get("name") else suffix_endpoint.split('.')[-1]

            if blue_print_attr.get("url_prefix"):
                # 自定义的蓝图 url
                url_pre = blue_print_attr.get("url_prefix")
            else:
                # 生成的蓝图 url
                url_pre = pretty.get_url_prefix(_end_point)

            # 注册蓝图并映射到endpoint
            app.register_blueprint(getattr(obj, name), url_prefix='{}'.format(url_pre))
        except Exception:
            logger.error(u'**** {0}\t module[{1}]'.format('fail', suffix_endpoint), exc_info=True)
        else:
            logger.info(u'**** {0}\t module[{1}]'.format('pass', suffix_endpoint))
    # print(app.url_map)
    return app

# APP = create_app()
