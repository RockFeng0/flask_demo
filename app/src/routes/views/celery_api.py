#! python3
# -*- encoding: utf-8 -*-

from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from app.com import code
from app.com.pretty import pretty_result
from job.celery_tasks import demo

task = Blueprint('task', __name__)


@task.route('/run', methods=['GET'])
def run():
    """ GET /tasks/run?seconds=10
        使用celery延时任务，模拟运行耗时的任务， seconds用于模拟运行时长
    """
    seconds = request.args.get("seconds", type=int)
    # apply_async中的可选参数**options，需参见celery官网
    # async_task = demo.add.apply_async(args=[2, 8], **options)
    async_task = demo.add.apply_async(args=[2, 8], eta=datetime.utcnow() + timedelta(seconds=seconds))
    return {"task id": async_task.id, "delay seconds": seconds}


@task.route('/running_status/<string:tid>', methods=['GET'])
def running_status(tid):
    """ GET /tasks/running_status/415644d0-c7ba-4d9d-8c40-d548f31899e2
    :param tid: celery生成的任务ID
    """
    try:
        back_end = demo.add.AsyncResult(tid)
    except Exception as e:
        print(e)
        return "---"
    status = {"state": back_end.state}
    print(status)
    if back_end.state == 'PENDING':
        status["message"] = "wait for the job finish."

    elif back_end.state == 'FAILURE':
        status["message"] = "something went wrong in the background job: " + str(back_end.info)

    else:
        status["message"] = "job finished."
        status["result"] = str(back_end.result)

    return status


@task.route('/deactivate/<string:tid>', methods=['GET'])
def deactivate(tid):
    """ GET /tasks/deactivate/415644d0-c7ba-4d9d-8c40-d548f31899e2
    取消激活celery的延时任务
    :param tid: celery生成的任务ID
    :return:
    """
    # celery 停止激活延时任务
    demo.celery.control.revoke(tid, terminate=True)
    return jsonify(pretty_result(code.OK))
