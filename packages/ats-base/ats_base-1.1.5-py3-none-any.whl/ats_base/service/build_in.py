"""
    内置函数
"""
from ats_base.base import req, entrance
from ats_base.common import func
from ats_base.config.configure import CONFIG

build_in = entrance.api(CONFIG.get(func.SERVICE, 'build_in'))


def handle(function: str, data):
    """
    内置函数
    :param module:
    :param function:
    :param data:
    :param url:
    :return:
    """
    result = req.post('{}/{}'.format(build_in, function), jsons=data)

    if result['code'] == 500:
        raise Exception(result['message'])

    return result['data']


