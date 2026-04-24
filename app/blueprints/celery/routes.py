#! python3
# -*- encoding: utf-8 -*-

from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from flask_restful.reqparse import RequestParser
from flask_login import login_required
from app.common import code
from app.common import pretty_result
from app.tasks.celery import celery_demo_task
from app.tasks.celery import celery

# 创建蓝图
bp = Blueprint(name='task', import_name=__name__, url_prefix="/task")


@bp.route('/run', methods=['GET'])
def run():
    """ GET /tasks/run?seconds=10
        使用celery延时任务，模拟运行耗时的任务， seconds用于模拟运行时长
    """
    parser = RequestParser()
    parser.add_argument('seconds', type=int, default=1, help='延迟执行的秒数', location='args')
    args = parser.parse_args()
    
    # 参数验证
    if args.seconds < 0:
        return jsonify(pretty_result(code.PARAM_ERROR, msg="秒数不能为负数"))
    
    async_task = celery_demo_task.add.apply_async(args=[2, 8], eta=datetime.utcnow() + timedelta(seconds=args.seconds))
    return jsonify(pretty_result(code.OK, data={"task_id": async_task.id, "delay_seconds": args.seconds}))


@bp.route('/run_high_priority', methods=['POST'])
def run_high_priority():
    """ POST /tasks/run_high_priority
        运行高优先级任务
    """
    parser = RequestParser()
    parser.add_argument('data', type=str, required=True, help='任务数据')
    args = parser.parse_args()
    
    # 参数验证
    if not args.data:
        return jsonify(pretty_result(code.PARAM_ERROR, msg="任务数据不能为空"))
    
    async_task = celery_demo_task.high_priority_task.apply_async(args=[args.data])
    return jsonify(pretty_result(code.OK, data={"task_id": async_task.id, "task_type": "high_priority"}))


@bp.route('/run_low_priority', methods=['POST'])
def run_low_priority():
    """ POST /tasks/run_low_priority
        运行低优先级任务
    """
    parser = RequestParser()
    parser.add_argument('data', type=str, required=True, help='任务数据')
    args = parser.parse_args()
    
    # 参数验证
    if not args.data:
        return jsonify(pretty_result(code.PARAM_ERROR, msg="任务数据不能为空"))
    
    async_task = celery_demo_task.low_priority_task.apply_async(args=[args.data])
    return jsonify(pretty_result(code.OK, data={"task_id": async_task.id, "task_type": "low_priority"}))


@bp.route('/status/<string:tid>', methods=['GET'])
def get_task_status(tid):
    """ GET /tasks/status/415644d0-c7ba-4d9d-8c40-d548f31899e2
    获取任务状态
    :param tid: celery生成的任务ID
    """
    try:
        # 验证任务ID格式
        if not tid or len(tid) < 10:
            return jsonify(pretty_result(code.PARAM_ERROR, msg="无效的任务ID"))
        
        back_end = celery.AsyncResult(tid)
        status = {"state": back_end.state}
        if back_end.state == 'PENDING':
            status["message"] = "任务等待中"
        elif back_end.state == 'FAILURE':
            status["message"] = f"任务执行失败: {str(back_end.info)}"
        elif back_end.state == 'RETRY':
            status["message"] = "任务重试中"
        elif back_end.state == 'STARTED':
            status["message"] = "任务执行中"
        else:
            status["message"] = "任务执行完成"
            status["result"] = back_end.result
        return jsonify(pretty_result(code.OK, data=status))
    except Exception as e:
        return jsonify(pretty_result(code.ERROR, msg=f"获取任务状态失败: {str(e)}"))


@bp.route('/cancel/<string:tid>', methods=['POST'])
def cancel_task(tid):
    """ POST /tasks/cancel/415644d0-c7ba-4d9d-8c40-d548f31899e2
    取消任务
    :param tid: celery生成的任务ID
    :return:
    """
    try:
        # 验证任务ID格式
        if not tid or len(tid) < 10:
            return jsonify(pretty_result(code.PARAM_ERROR, msg="无效的任务ID"))
        
        # celery 停止激活延时任务
        celery.control.revoke(tid, terminate=True)
        return jsonify(pretty_result(code.OK, msg="任务已取消"))
    except Exception as e:
        return jsonify(pretty_result(code.ERROR, msg=f"取消任务失败: {str(e)}"))


@bp.route('/workers', methods=['GET'])
def get_workers():
    """ GET /tasks/workers
    获取 worker 状态
    """
    try:
        inspect = celery.control.inspect()
        workers = inspect.active() or {}
        return jsonify(pretty_result(code.OK, data=workers))
    except Exception as e:
        return jsonify(pretty_result(code.ERROR, msg=f"获取 worker 状态失败: {str(e)}"))


@bp.route('/queues', methods=['GET'])
def get_queues():
    """ GET /tasks/queues
    获取队列状态
    """
    try:
        inspect = celery.control.inspect()
        queues = inspect.active_queues() or {}
        return jsonify(pretty_result(code.OK, data=queues))
    except Exception as e:
        return jsonify(pretty_result(code.ERROR, msg=f"获取队列状态失败: {str(e)}"))


@bp.route('/stats', methods=['GET'])
def get_stats():
    """ GET /tasks/stats
    获取 Celery 统计信息
    """
    try:
        inspect = celery.control.inspect()
        stats = inspect.stats() or {}
        return jsonify(pretty_result(code.OK, data=stats))
    except Exception as e:
        return jsonify(pretty_result(code.ERROR, msg=f"获取统计信息失败: {str(e)}"))


@bp.route('/registered', methods=['GET'])
def get_registered_tasks():
    """ GET /tasks/registered
    获取已注册的任务列表
    """
    try:
        inspect = celery.control.inspect()
        registered = inspect.registered() or {}
        return jsonify(pretty_result(code.OK, data=registered))
    except Exception as e:
        return jsonify(pretty_result(code.ERROR, msg=f"获取注册任务失败: {str(e)}"))


@bp.route('/scheduled', methods=['GET'])
def get_scheduled_tasks():
    """ GET /tasks/scheduled
    获取计划中的任务
    """
    try:
        inspect = celery.control.inspect()
        scheduled = inspect.scheduled() or {}
        return jsonify(pretty_result(code.OK, data=scheduled))
    except Exception as e:
        return jsonify(pretty_result(code.ERROR, msg=f"获取计划任务失败: {str(e)}"))


@bp.route('/active', methods=['GET'])
def get_active_tasks():
    """ GET /tasks/active
    获取正在执行的任务
    """
    try:
        inspect = celery.control.inspect()
        active = inspect.active() or {}
        return jsonify(pretty_result(code.OK, data=active))
    except Exception as e:
        return jsonify(pretty_result(code.ERROR, msg=f"获取活跃任务失败: {str(e)}"))


@bp.route('/reserved', methods=['GET'])
def get_reserved_tasks():
    """ GET /tasks/reserved
    获取已保留的任务
    """
    try:
        inspect = celery.control.inspect()
        reserved = inspect.reserved() or {}
        return jsonify(pretty_result(code.OK, data=reserved))
    except Exception as e:
        return jsonify(pretty_result(code.ERROR, msg=f"获取保留任务失败: {str(e)}"))