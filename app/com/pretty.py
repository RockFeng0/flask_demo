#! python3
# -*- encoding: utf-8 -*-

import re
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


def get_url_prefix(end_point):
    """
    生成待注册的蓝图 url
    :param end_point: 例如：xxx.api_1_0.xxx.xxx  和 celery_demo
    :return: /api/v1.0/xxx/xxx    和     /celery_demo
    """

    p = re.compile('(api)_([0-9]+)_([0-9]+)')
    _end_point_list = end_point.split('.')

    # e.g. ['api_1_0']
    api_matched_list = list(filter(lambda x: p.match(x), _end_point_list))

    if api_matched_list:
        # e.g. ['api_1_0', 'xxx']
        _url_prefix_list = _end_point_list[_end_point_list.index(api_matched_list[0]):]
        # e.g. /api/v1.0/xxx
        return p.sub(r'/\g<1>/v\g<2>.\g<3>', '/'.join(_url_prefix_list))
    else:
        return '/' + _end_point_list[-1]
