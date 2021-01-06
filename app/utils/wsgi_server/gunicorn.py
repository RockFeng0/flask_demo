#! python3
# -*- encoding: utf-8 -*-
import os
import multiprocessing
from abc import ABC

from gunicorn.six import iteritems
from gunicorn.app.base import BaseApplication
from app.config import ROOT_PATH


class GunicornConfig(object):
    """ gunicorn配置(Linux生产环境支持gunicorn) """
    bind = '127.0.0.1:5000'
    workers = multiprocessing.cpu_count() * 2 + 1
    worker_connections = 10000
    timeout = 60
    log_level = 'INFO'
    log_dir_path = os.path.join(ROOT_PATH, 'logs')
    log_file_max_bytes = 1024 * 1024 * 100
    log_file_backup_count = 10
    backlog = 64
    pid_file = 'run.pid'


class StandaloneApplication(BaseApplication, ABC):
    """
    gunicorn服务器启动类
    """

    def __init__(self, application, options):
        self.application = application
        self.options = options or {}
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application
