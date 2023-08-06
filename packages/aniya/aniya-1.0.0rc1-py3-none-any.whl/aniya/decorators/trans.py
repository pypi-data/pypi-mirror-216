from typing import Any

from aniya.decorators.base import combine_param
from aniya.err import VerifyError, PanicFmtData
from aniya.utils.undefined import check_undefined


def trans(key: str, tpc: Any, multi=False, allow_none=False):
    """
    :param key: 字符串key
    :param tpc: 类型类
    :param multi: key对应的value是否为多个
    :param allow_none: 是否允许为None
    """

    def middle(func):
        def inner(*args, **kwargs):
            params = combine_param(func, *args, **kwargs)
            if not multi:
                params = _trans(params, key, tpc, allow_none)
            else:
                params = _multi_trans(params, key, tpc, allow_none)
            result = func(**params)
            return result

        return inner

    return middle


def _trans(params, key, tpc, allow_none=False):
    value = params.get(key)
    if allow_none is None and allow_none is True:
        return params
    try:
        value = tpc(value)
    except TypeError:
        raise VerifyError('trans', PanicFmtData(key, tpc, value))
    params[key] = value
    return params


def _multi_trans(params, key, tpc, allow_none=False):
    values = check_undefined(params, key)
    if not isinstance(values, (list, tuple, set)):
        raise VerifyError('multi', PanicFmtData(key, None, values))
    trans_values = []
    for value in values:
        trans_param = _trans({key: value}, key, tpc, allow_none)
        trans_values.append(trans_param[key])
    params[key] = trans_values
    return params
