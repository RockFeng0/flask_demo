#! python3
# -*- encoding: utf-8 -*-
import os
import multiprocessing
from abc import ABC

from gunicorn.six import iteritems
from gunicorn.app.base import BaseApplication
from app.utils.log import server_log, error_log


class GunicornConfig(object):
    # gunicorn配置
    BIND = '0.0.0.0:5000'
    WORKERS = multiprocessing.cpu_count() * 2 + 1
    WORKER_CONNECTIONS = 10000
    BACKLOG = 64
    TIMEOUT = 60
    LOGLEVEL = 'INFO'
    ACCESSLOG = server_log
    ERRORLOG = error_log
    PID_FILE = 'run.pid'


class StandaloneApplication(BaseApplication, ABC):
    """
    gunicorn服务器启动类
    """

    def __init__(self, application):
        self.application = application
        self.options = {}
        for key in dir(GunicornConfig):
            if key.isupper():
                self.options[key.lower()] = getattr(GunicornConfig, key)

        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application
