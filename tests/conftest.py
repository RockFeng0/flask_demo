#! python3
# -*- encoding: utf-8 -*-

import pytest
import os



from app import create_app
from app.config import db, bcrypt, login_manager, scheduler, simple_cache


@pytest.fixture(scope="module")
def flask_app():
    """创建Flask应用实例"""
    flask_app = create_app()
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # 测试时使用内存
        "WTF_CSRF_ENABLED": False,  # 测试时禁用CSRF保护
        "SCHEDULER_API_ENABLED": False,  # 测试时禁用APScheduler API
    })
    
    # 在测试环境中禁用APScheduler和Celery
    import app.config.base
    app.config.base.scheduler = None
    
    # 禁用Celery路由，如果没有开启celery服务器
    flask_app.config['ALL_BLUE_PRINT'] = [
        {"app_module": "blueprints.auth", "attrs": {}},
        {"app_module": "blueprints.organization", "attrs": {}}
    ]

    if "memory" in flask_app.config["SQLALCHEMY_DATABASE_URI"]:
        # 创建数据库表
        with flask_app.app_context():
            db.create_all()
    
    yield flask_app

    if "memory" in flask_app.config["SQLALCHEMY_DATABASE_URI"]:
        # 清理数据库
        with flask_app.app_context():
            db.session.remove()
            db.drop_all()


@pytest.fixture(scope="module")
def client(flask_app):
    """创建测试客户端"""
    return flask_app.test_client()


@pytest.fixture(scope="module")
def runner(flask_app):
    """创建测试命令运行器"""
    return flask_app.test_cli_runner()