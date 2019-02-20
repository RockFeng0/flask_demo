import logging, importlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from flask_demo.demo.config import config, APP_ENV
from flask_demo.demo.log import console,log_handler,err_handler

logger = logging.getLogger(__name__)
logger.addHandler(console)
logger.setLevel(logging.DEBUG)

db = SQLAlchemy()
cors = CORS()

def create_app():
    app = Flask(__name__)
    configuration = config[APP_ENV]
    
    if APP_ENV == 'production':
        logger.addHandler(log_handler)
        logger.addHandler(err_handler)

    # 将配置读取到flask对象中
    app.config.from_object(configuration)
    configuration.init_app(app)
    db.init_app(app)
    cors.init_app(app, supports_credentials=True)
            
    blue_prints = app.config.get("ALL_BLUE_PRINT")
    for module_name,module_switch in blue_prints.items():        
        if module_switch:
            try:
                obj = importlib.import_module("flask_demo.demo.views.{0}".format(module_name))
                app.register_blueprint(getattr(obj,module_name), url_prefix = '/{}'.format(module_name))
            except Exception as e:
                logger.error('Launch fail:\t{0}'.format(module_name))
                logger.exception(e)
            else:
                logger.info('Launch ok:\t{0}'.format(module_name))

    return app

app = create_app()


from .views.views import *
