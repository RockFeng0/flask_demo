#! python3
# -*- encoding: utf-8 -*-

import logging
from app.tasks.celery import celery

# 配置日志
logger = logging.getLogger(__name__)


# celery 生产消费者模型
@celery.task(
    queue='default',
    priority=5,
    retry_kwargs={'max_retries': 3, 'countdown': 10},
    autoretry_for=(Exception,),
    time_limit=300,
    bind=True
)
def add(self, x, y):
    """简单的加法任务"""
    try:
        logger.info(f"开始执行加法任务: {x} + {y}")
        result = x + y
        logger.info(f"加法任务执行完成: {x} + {y} = {result}")
        return result
    except Exception as e:
        logger.error(f"加法任务执行失败: {e}")
        # 手动重试
        self.retry(exc=e, countdown=10, max_retries=3)


@celery.task(
    queue='high',
    priority=10,
    retry_kwargs={'max_retries': 5, 'countdown': 5},
    autoretry_for=(Exception,),
    time_limit=60,
    bind=True
)
def high_priority_task(self, data):
    """高优先级任务"""
    try:
        logger.info(f"开始执行高优先级任务: {data}")
        # 处理高优先级任务的逻辑
        result = f"处理高优先级任务: {data}"
        logger.info(f"高优先级任务执行完成: {result}")
        return result
    except Exception as e:
        logger.error(f"高优先级任务执行失败: {e}")
        # 手动重试
        self.retry(exc=e, countdown=5, max_retries=5)


@celery.task(
    queue='low',
    priority=1,
    retry_kwargs={'max_retries': 2, 'countdown': 30},
    autoretry_for=(Exception,),
    time_limit=600,
    bind=True
)
def low_priority_task(self, data):
    """低优先级任务"""
    try:
        logger.info(f"开始执行低优先级任务: {data}")
        # 处理低优先级任务的逻辑
        result = f"处理低优先级任务: {data}"
        logger.info(f"低优先级任务执行完成: {result}")
        return result
    except Exception as e:
        logger.error(f"低优先级任务执行失败: {e}")
        # 手动重试
        self.retry(exc=e, countdown=30, max_retries=2)