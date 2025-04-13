#! python3
# -*- encoding: utf-8 -*-

import os
from typing import List
import importlib
from loguru import logger

from flask import Flask
from com import pretty
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


def register_blueprints(app:Flask, modules:List[dict], prefix:str):
    """
    :param app: Flask app 对象
    :param modules: 应用模块蓝图对象的路径
    :param prefix: 应用模块前缀，默认为app
    """

    # 处理蓝图
    for module in modules:
        _endpoint_suffix, blue_print_attr = module["app_module"], module["attrs"]

        if blue_print_attr.pop("is_off"):
            continue

        # noinspection PyBroadException
        try:
            # 引入模块
            mod = importlib.import_module(f"{prefix}.{_endpoint_suffix}.routes")
            # 使用config中的参数注册蓝图（如果创建蓝图时填了同样的参数，则会被覆盖。）
            # 可以通过config自定义蓝图的name和url_prefix参数
            app.register_blueprint(mod.bp, **blue_print_attr)

        except Exception as e:
            logger.error(f'**** fail\t module[{_endpoint_suffix}]')
            # logger.exception("error?")  # 打印堆栈信息
        else:
            logger.info(f'**** pass\t module[{_endpoint_suffix}]')
    # print(app.url_map)


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
    # blue_prints = app.config.get("ALL_BLUE_PRINT")
    # prefix_endpoint = app.config.get("PREFIX_ENDPOINT")
    # for suffix_endpoint, blue_print_attr in blue_prints.items():
    #     # 开关是关闭的就跳过
    #     if blue_print_attr.get("is_off"):
    #         continue
    #
    #     # noinspection PyBroadException
    #     try:
    #         # 生成url前缀
    #         _end_point = "{0}.{1}".format(prefix_endpoint, suffix_endpoint)
    #         obj = importlib.import_module(_end_point)
    #
    #         if blue_print_attr.get("name") and blue_print_attr.get("url_prefix"):
    #             # 自定义的蓝图
    #             name = blue_print_attr.get("name")
    #             url_pre = blue_print_attr.get("url_prefix")
    #         else:
    #             # 生成的蓝图
    #             name = suffix_endpoint.split('.')[-1]
    #             url_pre = pretty.get_url_prefix(_end_point)
    #
    #         # 注册蓝图并映射到endpoint
    #         app.register_blueprint(getattr(obj, name), url_prefix='{}'.format(url_pre))
    #     except Exception as e:
    #         logger.error(u'**** {0}\t module[{1}]'.format('fail', suffix_endpoint))
    #         logger.exception("error?")  # 打印堆栈信息
    #     else:
    #         logger.info(u'**** {0}\t module[{1}]'.format('pass', suffix_endpoint))
    blue_prints = app.config.get("ALL_BLUE_PRINT")
    prefix_endpoint = app.config.get("PREFIX_ENDPOINT")
    register_blueprints(app, modules=blue_prints, prefix=prefix_endpoint)
    return app


# APP = create_app()
