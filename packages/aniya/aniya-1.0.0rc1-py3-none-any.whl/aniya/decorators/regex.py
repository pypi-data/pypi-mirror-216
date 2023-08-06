import re

from aniya.decorators.base import combine_param
from aniya.err import VerifyError, PanicFmtData
from aniya.utils.undefined import check_undefined


def regex(key: str, pattern: str, multi=False):
    """
    正则
    :param key: 校验的参数
    :param pattern: 正则规则
    :param multi: key对应的value是否为多个
    """

    def middle(func):
        def inner(*args, **kwargs):
            params = combine_param(func, *args, **kwargs)
            if not multi:
                _regex(params, key, pattern)
            else:
                _multi_regex(params, key, pattern)
            result = func(**params)
            return result

        return inner

    return middle


def _regex(params, key, pattern):
    value = check_undefined(params, key)

    if not isinstance(value, str):
        raise VerifyError('string', PanicFmtData(key, pattern, value))

    match_success = re.match(pattern, value)
    if not match_success:
        raise VerifyError('regex', PanicFmtData(key, pattern, value))


def _multi_regex(params, key, pattern):
    values = check_undefined(params, key)
    if not isinstance(values, (list, tuple, set)):
        raise VerifyError('multi', PanicFmtData(key, None, values))
    for value in values:
        _regex({key: value}, key, pattern)
