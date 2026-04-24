#! python3
# -*- encoding: utf-8 -*-

import os
from .base import (
    Config,
    cors,
    db,
    login_manager,
    bcrypt,
    simple_cache,
    migrate,
    scheduler,
    csrf,
    ROOT_PATH,
)
from .dev import DevConfig
from .prod import ProdConfig

# 配置使用的环境， 测试环境或生产环境
APP_ENV = os.getenv("APP_ENV", "testing")

configs = {"production": ProdConfig, "testing": DevConfig}

__all__ = [
    "Config",
    "DevConfig",
    "ProdConfig",
    "APP_ENV",
    "configs",
    "cors",
    "db",
    "login_manager",
    "bcrypt",
    "simple_cache",
    "migrate",
    "scheduler",
    "csrf",
    "ROOT_PATH",
]
