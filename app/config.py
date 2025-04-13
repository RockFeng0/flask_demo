#! python3
# -*- encoding: utf-8 -*-

import os
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

# 配置使用的环境， 测试环境或生产环境
APP_ENV = 'testing'
# APP_ENV = 'production'

# 设置根路径(e.g. /opt/deploy/flask_demo, c:\flask_demo)
ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

# 创建跨域对象： 解决跨域问题
cors = CORS()

# 创建数据库对象： 处理数据库对象关系映射
db = SQLAlchemy()

# 创建登录管理对象： 处理用户登录
login_manager = LoginManager()

# 创建加密对象： 处理用户登录密码
bcrypt = Bcrypt()

# 创建一个缓存对象
simple_cache = Cache()

# 创建一个数据库迁移对象
migrate = Migrate()

# 创建计划任务对象： 处理定时任务
scheduler = APScheduler()


class Config(object):
    # flask 防止返回的json中汉字被转码
    JSON_AS_ASCII = False
    SECRET_KEY = 'lskdjflsj'

    # flask-login
    TOKEN_LIFETIME = 3600
    REMEMBER_COOKIE_NAME = "token"

    # flask-sqlalchemy 数据库
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False  # 请求执行完逻辑之后自动提交，而不用我们每次都手动调用session.commit(); 我还是习惯，自己 commit
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 需要设定参数True 或者 Flase,是说SQLALCHEMY_TRACK_MODIFICATIONS不能默认什么都没有

    # flask-apscheduler
    SCHEDULER_EXECUTORS = { # 线程池配置
        'default': {'type': 'threadpool', 'max_workers': 20}
    }
    SCHEDULER_JOB_DEFAULTS = { # 预设任务配置
        'coalesce': False,
        'max_instances': 3
    }
    SCHEDULER_API_ENABLED = True  # 启用apscheduler api的开关

    # flask-caching
    CACHE_TYPE = 'SimpleCache'  # 使用简单内存缓存。 Flask-Caching支持多种缓存类型，具体参见官网
    CACHE_DEFAULT_TIMEOUT = 300  # 默认缓存超时时间（秒）

    # 蓝图映射endpoint的前缀
    PREFIX_ENDPOINT = "app"

    # 蓝图开关
    # ALL_BLUE_PRINT = {
    #     "api.user": {"is_off": False},
    #     "api.api_1_0.organization": {"is_off": False},
    #     "views.celery_api": {"is_off": False, "url_prefix": "/task", "name": "task"},
    # }
    ALL_BLUE_PRINT = [
        {
            "app_module": "auth_demo",
            "attrs":{"is_off": False}
        },
        {
            "app_module": "organization_demo",
            "attrs":{"is_off": False}
        },
        {
            "app_module": "celery_demo",
            "attrs":{"is_off": False, "url_prefix": "/task", "name": "task"}
        },
    ]

    @staticmethod
    def init_app(app):
        cors.init_app(app, supports_credentials=True)
        db.init_app(app)
        login_manager.init_app(app)
        bcrypt.init_app(app)
        simple_cache.init_app(app)
        migrate.init_app(app, db)
        scheduler.init_app(app)
        scheduler.start()


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
    # SCHEDULER_JOBSTORES = {
    #     'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
    # }


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
