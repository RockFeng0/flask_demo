#! python3
# -*- encoding: utf-8 -*-


from app.celery_demo import celery

# celery 生产消费者模型
@celery.task()
def add(x, y):
    return x+y
