from aniya.decorators.base import combine_param
from aniya.err import VerifyError, PanicFmtData
from aniya.utils.undefined import check_undefined


def length(key: str, min_length: int = None, max_length: int = None, multi=False, allow_none=False):
    """
    长度
    :param key: 字符串key
    :param min_length: 最小长度
    :param max_length: 最大长度
    :param multi: key对应的value是否为多个
    :param allow_none: 是否允许为None，如果为None，则将长度定义为0
    """

    def middle(func):
        def inner(*args, **kwargs):
            params = combine_param(func, *args, **kwargs)
            if not multi:
                _length(params, key, min_length, max_length, allow_none)
            else:
                _multi_length(params, key, min_length, max_length, allow_none)
            result = func(**params)
            return result

        return inner

    return middle


def _length(params, key, min_length=None, max_length=None, allow_none=False):
    value = check_undefined(params, key)

    # 获取数据的长度
    if value is None and allow_none is True:
        value_length = 0
    else:
        if not (hasattr(value, '__len__') and callable(getattr(value, '__len__'))):
            raise VerifyError('len', PanicFmtData(key, None, None))
        value_length = len(value)

    # 最小值
    if min_length is not None and value_length < min_length:
        raise VerifyError('min_length', PanicFmtData(key, min_length, value_length))

    # 最大值
    if max_length is not None and value_length > max_length:
        raise VerifyError('max_length', PanicFmtData(key, max_length, value_length))


def _multi_length(params, key, min_length=None, max_length=None, allow_none=False):
    values = check_undefined(params, key)
    if not isinstance(values, (list, tuple, set)):
        raise VerifyError('multi', PanicFmtData(key, None, values))
    for value in values:
        _length({key: value}, key, min_length, max_length, allow_none)
