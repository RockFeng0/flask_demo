#! python3
# -*- encoding: utf-8 -*-


from job import celery


@celery.task()
def add(x, y):
    return x+y
