#! python3
# -*- encoding: utf-8 -*-

import logging

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db

APP = create_app()

migrate = Migrate(APP, db)

manager = Manager(APP)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    """
    生产模式启动命令函数
    To use: python3 manager.py run
    """
    from utils import StandaloneApplication

    # APP.logger.setLevel(APP.config.get('LOG_LEVEL', logging.INFO))
    # service_config = {
    #     'bind': APP.config.get('BIND', '0.0.0.0:5000'),
    #     'workers': APP.config.get('WORKERS', cpu_count() * 2 + 1),
    #     'worker_class': 'gevent',
    #     'worker_connections': APP.config.get('WORKER_CONNECTIONS', 10000),
    #     'backlog': APP.config.get('BACKLOG', 2048),
    #     'timeout': APP.config.get('TIMEOUT', 60),
    #     'loglevel': APP.config.get('LOG_LEVEL', 'info'),
    #     'pidfile': APP.config.get('PID_FILE', 'run.pid'),
    # }
    # StandaloneApplication(APP, service_config).run()
    StandaloneApplication(APP).run()


@manager.command
def debug():
    """
    debug模式启动命令函数
    To use: python3 manager.py debug
    """
    APP.logger.setLevel(logging.DEBUG)
    APP.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == "__main__":
    manager.run()
