#! python3
# -*- encoding: utf-8 -*-

import logging
# from multiprocessing import cpu_count

from app import create_app
from app.views import index

APP = create_app()
APP.add_url_rule('/', endpoint='index', view_func=index, methods=["GET"])


@APP.cli.command("serve")
def serve():
    """
    生产模式启动命令函数
    To use: flask serve
    """
    from utils.wsgi_server.gunicorn import StandaloneApplication

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

if __name__ == "__main__":
    APP.logger.setLevel(logging.DEBUG)
    APP.run(host='0.0.0.0', port=5000, debug=True)
