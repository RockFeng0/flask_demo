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
from flask_wtf.csrf import CSRFProtect
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置根路径(e.g. /opt/deploy/flask_demo, c:\flask_demo)
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

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

# 创建CSRF保护对象
csrf = CSRFProtect()


class Config(object):
    # flask 防止返回的json中汉字被转码
    JSON_AS_ASCII = False
    SECRET_KEY = os.getenv("SECRET_KEY", "lskdjflsj")

    # 安全头部配置
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True  # 在生产环境中启用
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True  # 在生产环境中启用
    PERMANENT_SESSION_LIFETIME = 3600

    # flask-login
    TOKEN_LIFETIME = 3600
    REMEMBER_COOKIE_NAME = "token"

    # flask-sqlalchemy 数据库
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False  # 请求执行完逻辑之后自动提交，而不用我们每次都手动调用session.commit(); 我还是习惯，自己 commit
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 需要设定参数True 或者 Flase,是说SQLALCHEMY_TRACK_MODIFICATIONS不能默认什么都没有

    # flask-apscheduler
    SCHEDULER_EXECUTORS = {  # 线程池配置
        "default": {"type": "threadpool", "max_workers": 20}
    }
    SCHEDULER_JOB_DEFAULTS = {"coalesce": False, "max_instances": 3}  # 预设任务配置
    SCHEDULER_API_ENABLED = True  # 启用apscheduler api的开关

    # flask-caching
    CACHE_TYPE = "RedisCache"  # 使用Redis缓存
    CACHE_REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_DEFAULT_TIMEOUT = 300  # 默认缓存超时时间（秒）

    # 蓝图映射endpoint的前缀
    PREFIX_ENDPOINT = "app"

    # 蓝图开关
    ALL_BLUE_PRINT = [
        {"app_module": "blueprints.auth", "attrs": {"is_off": False}},
        {"app_module": "blueprints.organization", "attrs": {"is_off": False}},
        {
            "app_module": "blueprints.celery",
            "attrs": {"is_off": False, "url_prefix": "/task", "name": "task"},
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
        if scheduler:
            scheduler.init_app(app)
            scheduler.start()
        csrf.init_app(app)
