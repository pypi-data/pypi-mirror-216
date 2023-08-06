from decimal import Decimal

from aniya.decorators.base import combine_param
from aniya.err import VerifyError, PanicFmtData
from aniya.utils.undefined import check_undefined


def digits(key: str, decimals: int, multi=False):
    """
    小数进位
    :param key: 字符串key
    :param decimals: 保留位数
    :param multi: key对应的value是否为多个
    """

    def middle(func):
        def inner(*args, **kwargs):
            params = combine_param(func, *args, **kwargs)
            if not multi:
                params = _digits(params, key, decimals)
            else:
                params = _multi_digits(params, key, decimals)
            result = func(**params)

            return result

        return inner

    return middle


def _digits(params, key, decimals):
    value = check_undefined(params, key)
    if not isinstance(value, (int, float, Decimal)):
        raise VerifyError('number', PanicFmtData(key, None, value))
    params[key] = round(value, decimals)
    return params


def _multi_digits(params, key, decimals):
    values = check_undefined(params, key)
    if not isinstance(values, (list, tuple, set)):
        raise VerifyError('multi', PanicFmtData(key, None, values))
    digits_values = []
    for value in values:
        digits_param = _digits({key: value}, key, decimals)
        digits_values.append(digits_param[key])
    params[key] = digits_values
    return params
