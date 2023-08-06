from aniya.decorators.base import combine_param
from aniya.err import VerifyError, PanicFmtData
from aniya.utils.undefined import check_undefined


def exclude(key: str, values, multi=False):
    """
    不包括
    :param key: 字符串key
    :param values: 不包括的值
    :param multi: key对应的value是否为多个
    """

    def middle(func):
        def inner(*args, **kwargs):
            params = combine_param(func, *args, **kwargs)
            if not multi:
                _exclude(params, key, values)
            else:
                _multi_exclude(params, key, values)
            result = func(**params)
            return result

        return inner

    return middle


def _exclude(params, key, values):
    value = check_undefined(params, key)
    if value in values:
        raise VerifyError('exclude', PanicFmtData(key, values, value))


def _multi_exclude(params, key, values):
    vs = check_undefined(params, key)
    if not isinstance(vs, (list, tuple, set)):
        raise VerifyError('multi', PanicFmtData(key, None, vs))
    for v in vs:
        _exclude({key: v}, key, values)
