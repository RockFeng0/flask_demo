#! python3
# -*- encoding: utf-8 -*-

from app.com.code import CODE_MSG_MAP


def pretty_result(code, msg=None, data=None):
    """
    格式化的响应
    :param data:  本次请求的响应体
    :param code: 响应码， 默认值200，表示成功
    :param msg: 响应码的描述
    """
    return {
        'code': code,
        'msg': msg if msg is not None else CODE_MSG_MAP.get(code),
        'data': data
    }
