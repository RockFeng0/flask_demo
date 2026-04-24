#! python3
# -*- encoding: utf-8 -*-

import sys
from celery import Celery

from app.config import APP_ENV
from app.tasks.celery.conf import configs

celery = Celery("flask_demo")
celery.config_from_object(configs[APP_ENV])
sys.path.insert(0, "") if "" not in sys.path else None

# Celery 任务子包
# from . import celery_demo_task