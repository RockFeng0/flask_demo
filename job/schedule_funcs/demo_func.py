#! python3
# -*- encoding: utf-8 -*-

from datetime import datetime, timedelta

from job.celery_tasks import demo


def add_task(a, b):
    async_task = demo.add.apply_async(args=(a, b), eta=datetime.utcnow() + timedelta(seconds=20))
    print({"task id": async_task.id, "delay seconds": 10})
    return {"task id": async_task.id, "delay seconds": 10}
