#! python3
# -*- encoding: utf-8 -*-

import os
import importlib
from loguru import logger
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

# from flask_login import LoginManager
# from flask_bcrypt import Bcrypt

from app import pretty
from app.config import ROOT_PATH, APP_ENV, configs

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


def _init_log():
    """
    配置日志对象
    """
    logs_path = os.path.join(ROOT_PATH, 'logs')

    if not os.path.exists(logs_path):
        os.mkdir(logs_path)

    server_log = os.path.join(logs_path, "server_{time:YYYY-MM-DD}.log")
    error_log = os.path.join(logs_path, "error_{time:YYYY-MM-DD}.log")

    server_sink = logger.add(sink=server_log, level="DEBUG", rotation="1 day")
    error_sink = logger.add(sink=error_log, level="ERROR", rotation="1 day")
    return server_sink, error_sink


def create_app():
    """
    创建app
    """
    app = Flask(__name__)
    configuration = configs[APP_ENV]

    # 将配置读取到flask对象中
    app.config.from_object(configuration)

    # 初始化日志对象
    _init_log()

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
