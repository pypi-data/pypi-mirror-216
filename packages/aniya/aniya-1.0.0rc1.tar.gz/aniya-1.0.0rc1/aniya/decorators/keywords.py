from aniya.decorators.base import combine_param
from aniya.err import VerifyError, PanicFmtData
from aniya.utils.undefined import check_undefined


def include_keys(key: str, values: set):
    """
    字典key中必须包含这些值
    :param key: 字符串key
    :param values: 不包括的值
    """

    def middle(func):
        def inner(*args, **kwargs):
            params = combine_param(func, *args, **kwargs)
            _include_keys(params, key, values)
            result = func(**params)

            return result

        return inner

    return middle


def exclude_keys(key: str, values):
    """
    字典key中不能包含这些值
    :param key: 字符串key
    :param values: 不包括的值
    """

    def middle(func):
        def inner(*args, **kwargs):
            params = combine_param(func, *args, **kwargs)
            _exclude_keys(params, key, values)
            result = func(**params)

            return result

        return inner

    return middle


def _include_keys(params, key, values):
    value = check_undefined(params, key)
    param_keys = set(value.keys())
    if not values.issubset(param_keys):
        raise VerifyError('include_keys', PanicFmtData(key, values, value))


def _exclude_keys(params, key, values):
    value = check_undefined(params, key)
    param_keys = set(value.keys())
    if param_keys & values:
        raise VerifyError('exclude_keys', PanicFmtData(key, values, value))
