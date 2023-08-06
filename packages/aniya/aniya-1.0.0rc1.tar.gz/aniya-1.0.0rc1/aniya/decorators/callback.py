from typing import Callable, List, Union

from aniya.decorators.base import combine_param
from aniya.utils.undefined import check_undefined


def callback(key: str, calls: Union[Callable, List[Callable]]):
    """
    将指定值作为参数回调，函数入参为key对应的值，出参也为key对应的值
    :param key: 校验的参数
    :param calls: 回调函数
    """

    def middle(func):
        def inner(*args, **kwargs):
            params = combine_param(func, *args, **kwargs)
            params = _callback(params, key, calls)
            result = func(**params)
            return result

        return inner

    return middle


def _callback(params, key, calls):
    value = check_undefined(params, key)
    if isinstance(calls, (list, tuple, set)):
        for call in calls:
            value = call(value)
    else:
        value = calls(value)
    params[key] = value
    return params
