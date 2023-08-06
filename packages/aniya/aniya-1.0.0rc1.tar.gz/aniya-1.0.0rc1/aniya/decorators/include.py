from typing import Union

from aniya.decorators.base import combine_param
from aniya.err import VerifyError, PanicFmtData
from aniya.utils.undefined import check_undefined


def include(key: str, values: Union[tuple, list, set], multi=False):
    """
    包括
    :param key: 字符串key
    :param values: 包括的值
    :param multi: key对应的value是否为多个
    """

    def middle(func):
        def inner(*args, **kwargs):
            params = combine_param(func, *args, **kwargs)
            if not multi:
                _include(params, key, values)
            else:
                _multi_include(params, key, values)
            result = func(**params)
            return result

        return inner

    return middle


def _include(params, key, values):
    value = check_undefined(params, key)
    if value not in values:
        raise VerifyError('include', PanicFmtData(key, values, value))


def _multi_include(params, key, values):
    vs = check_undefined(params, key)
    if not isinstance(vs, (list, tuple, set)):
        raise VerifyError('multi', PanicFmtData(key, None, vs))
    for v in vs:
        _include({key: v}, key, values)
