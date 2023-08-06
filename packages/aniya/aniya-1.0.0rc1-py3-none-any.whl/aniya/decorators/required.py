from aniya.decorators.base import combine_param
from aniya.err import VerifyError, PanicFmtData
from aniya.utils.undefined import undefined


def required(key: str, null_values=(undefined, None)):
    """
    是否必须
    作为函数装饰器验证函数参数的时候，用处不大。
    :param key: 字符串key
    :param null_values: null值列表
    """

    def middle(func):
        def inner(*args, **kwargs):
            params = combine_param(func, *args, **kwargs)
            _required(params, key, null_values)
            result = func(**params)
            return result

        return inner

    return middle


def _required(params, key, null_values=(undefined, None)):
    value = params.get(key, undefined)
    if value in null_values:
        raise VerifyError('required', PanicFmtData(key, null_values, value))
