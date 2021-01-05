#! python3
# -*- encoding: utf-8 -*-

import os
import multiprocessing

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

# 配置使用的环境， 测试环境或生产环境
APP_ENV = 'testing'
# APP_ENV = 'production'

# 设置根路径(e.g. /opt/deploy/flask_demo, c:\flask_demo)
ROOT_PATH = os.path.dirname(os.path.dirname(__file__))


class Config(object):
    # flask 防止返回的json中汉字被转码
    JSON_AS_ASCII = False
    SECRET_KEY = 'lskdjflsj'

    # flask-login
    TOKEN_LIFETIME = 3600
    REMEMBER_COOKIE_NAME = "token"

    # flask-sqlalchemy 数据库 - 请求执行完逻辑之后自动提交，而不用我们每次都手动调用session.commit(); 我还是习惯，自己 commit
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False

    # flask-sqlalchemy 数据库 - 需要设定参数True 或者 Flase,是说SQLALCHEMY_TRACK_MODIFICATIONS不能默认什么都没有
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # flask-apscheduler  线程池配置
    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }

    # flask-apscheduler 预设任务配置
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 3
    }

    # flask-apscheduler 启用apscheduler api的开关
    SCHEDULER_API_ENABLED = True

    # 蓝图映射endpoint的前缀
    PREFIX_ENDPOINT = "app.src.routes"

    # 蓝图开关
    ALL_BLUE_PRINT = {
        "api_0_0.rm_task": {"is_off": True, "url_prefix": "/rm_task"},
        "views.celery_api": {"is_off": False, "url_prefix": "/task", "name": "task"},
        "api_1_0.organization": {"is_off": False},
    }

    @staticmethod
    def init_app(app):
        pass


class ProdConfig(Config):
    # sqlalchemy mysql
    USERNAME = "username"
    PASSWORD = "password"
    HOST = "xxx.xxx.xxx.xxx"
    PORT = 3306
    DATABASE = 'flask_demo'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'. \
        format(USERNAME, PASSWORD, HOST, PORT, DATABASE)

    # flask-apscheduler 存储的位置,用于定时任务的持久化
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
    }

    # gunicorn配置
    BIND = '127.0.0.1:5000'
    WORKERS = multiprocessing.cpu_count() * 2 + 1
    WORKER_CONNECTIONS = 10000
    BACKLOG = 64
    TIMEOUT = 60
    LOG_LEVEL = 'INFO'
    LOG_DIR_PATH = os.path.join(ROOT_PATH, 'logs')
    LOG_FILE_MAX_BYTES = 1024 * 1024 * 100
    LOG_FILE_BACKUP_COUNT = 10
    PID_FILE = 'run.pid'


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


configs = {"production": ProdConfig, "testing": DevConfig}
