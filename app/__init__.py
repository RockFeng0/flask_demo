#! python3
# -*- encoding: utf-8 -*-

import os
import importlib
from loguru import logger

from flask import Flask
from app.com import pretty
from app.config import APP_ENV, ROOT_PATH, configs


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

    # 初始化日志
    _init_log()

    # 对象的初始化
    configuration.init_app(app)

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

            if blue_print_attr.get("name") and blue_print_attr.get("url_prefix"):
                # 自定义的蓝图
                name = blue_print_attr.get("name")
                url_pre = blue_print_attr.get("url_prefix")
            else:
                # 生成的蓝图
                name = suffix_endpoint.split('.')[-1]
                url_pre = pretty.get_url_prefix(_end_point)

            # 注册蓝图并映射到endpoint
            app.register_blueprint(getattr(obj, name), url_prefix='{}'.format(url_pre))
        except Exception as e:
            logger.error(u'**** {0}\t module[{1}]'.format('fail', suffix_endpoint))
            # logger.exception("error?")  # 打印堆栈信息
        else:
            logger.info(u'**** {0}\t module[{1}]'.format('pass', suffix_endpoint))
    return app

# APP = create_app()
