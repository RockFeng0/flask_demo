#! python3
# -*- encoding: utf-8 -*-

import re
from app.code import CODE_MSG_MAP


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


def get_url_prefix(end_point):
    """
    获取待注册蓝图URL
    :return: app.views.api_1_0.org  --> /api/v1.0/org
    :return: app.views.celery_demo  --> /celery_demo
    """
    p = re.compile('(api)_([0-9]+)_([0-9]+)')
    _end_point_list = end_point.split('.')

    _api_point_list = list(filter(lambda x: p.match(x), _end_point_list))

    if _api_point_list:
        _url_prefix_list = _end_point_list[_end_point_list.index(_api_point_list[0]):]
        return p.sub(r'/\g<1>/v\g<2>.\g<3>', '/'.join(_url_prefix_list))
    else:
        return "/" + _end_point_list[-1]
