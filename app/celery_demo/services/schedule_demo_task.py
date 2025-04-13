#! python3
# -*- encoding: utf-8 -*-

from datetime import datetime, timedelta

from app.celery_demo.services import celery_demo_task


def add_task(a, b):
    """ 定时调度插件  Flask-APScheduler
    仍然要使用celery的生产消费者模型的异步任务，但是要使用插件自带的Schedule Job API
    """
    async_task = celery_demo_task.add.apply_async(args=(a, b), eta=datetime.utcnow() + timedelta(seconds=20))
    print({"task id": async_task.id, "delay seconds": 10})
    return {"task id": async_task.id, "delay seconds": 10}
