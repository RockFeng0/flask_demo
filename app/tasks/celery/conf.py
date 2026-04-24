#! python3
# -*- encoding: utf-8 -*-

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config(object):
    # 基础配置
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_ENABLE_UTC = True

    # 任务序列化
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']

    # 任务执行配置
    CELERYD_FORCE_EXECV = True  # 防止死锁
    CELERYD_MAX_TASKS_PER_CHILD = 100  # 每个worker最多执行100个任务被销毁，防止内存泄漏
    CELERYD_TASK_TIME_LIMIT = 300  # 任务执行超时时间（秒）

    # Broker配置
    BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 43200}  # 延时任务可见性超时时间

    # 结果配置
    CELERY_RESULT_EXPIRES = 3600  # 结果过期时间（秒）

    # 并发配置
    CELERYD_CONCURRENCY = 4  # 并发worker数量
    CELERYD_PREFETCH_MULTIPLIER = 1  # 任务预取倍数，1表示一次只获取一个任务，适合IO密集型任务

    # 任务压缩
    CELERY_MESSAGE_COMPRESSION = 'gzip'  # 任务消息压缩

    # 任务路由
    CELERY_ROUTES = {
        'app.tasks.celery.celery_demo_task.add': {
            'queue': 'default'
        },
        'app.tasks.celery.celery_demo_task.high_priority_task': {
            'queue': 'high'
        },
        'app.tasks.celery.celery_demo_task.low_priority_task': {
            'queue': 'low'
        }
    }

    # 任务队列
    CELERY_QUEUES = {
        'default': {
            'exchange': 'default',
            'exchange_type': 'direct',
            'routing_key': 'default'
        },
        'high': {
            'exchange': 'high',
            'exchange_type': 'direct',
            'routing_key': 'high.priority'
        },
        'low': {
            'exchange': 'low',
            'exchange_type': 'direct',
            'routing_key': 'low.priority'
        }
    }

    # 任务导入
    CELERY_IMPORTS = (
        "app.tasks.celery.celery_demo_task"
    )


class ProdConfig(Config):
    # 从环境变量获取配置
    BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://172.16.1.1:6379')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://172.16.1.1:6379')


class DevConfig(Config):
    # 从环境变量获取配置
    BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://:123456@127.0.0.1:6379')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://:123456@127.0.0.1:6379/0')


configs = {"production": ProdConfig, "testing": DevConfig}