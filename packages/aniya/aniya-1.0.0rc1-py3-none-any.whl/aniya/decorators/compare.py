from aniya.decorators.base import combine_param
from aniya.err import VerifyError, PanicFmtData
from aniya.utils.undefined import check_undefined


def compare(key: str, gt=None, gte=None, lt=None, lte=None, multi=False):
    """
    大小比较
    :param key: 字符串key
    :param gt: 大于
    :param gte: 大于等于
    :param lt: 小于
    :param lte: 小于等于
    :param multi: key对应的value是否为多个
    """

    def middle(func):
        def inner(*args, **kwargs):
            params = combine_param(func, *args, **kwargs)
            if not multi:
                _compare(params, key, gt, gte, lt, lte)
            else:
                _multi_compare(params, key, gt, gte, lt, lte)
            result = func(**params)

            return result

        return inner

    return middle


def _compare(params, key, gt=None, gte=None, lt=None, lte=None):
    value = check_undefined(params, key)

    if gt is not None:
        try:
            if value <= gt:
                raise VerifyError('gt', PanicFmtData(key, gt, value))
        except TypeError:
            raise VerifyError('compare', PanicFmtData(key, gt, value))

    if gte is not None:
        try:
            if value < gte:
                raise VerifyError('gte', PanicFmtData(key, gte, value))
        except TypeError:
            raise VerifyError('compare', PanicFmtData(key, gte, value))

    elif lt is not None:
        try:
            if value >= lt:
                raise VerifyError('lt', PanicFmtData(key, lt, value))
        except TypeError:
            raise VerifyError('compare', PanicFmtData(key, lt, value))

    elif lte is not None:
        try:
            if value > lte:
                raise VerifyError('lte', PanicFmtData(key, lte, value))
        except TypeError:
            raise VerifyError('compare', PanicFmtData(key, lte, value))


def _multi_compare(params, key, gt=None, gte=None, lt=None, lte=None):
    values = check_undefined(params, key)
    if not isinstance(values, (list, tuple, set)):
        raise VerifyError('multi', PanicFmtData(key, None, values))

    for value in values:
        _compare({key: value}, key, gt, gte, lt, lte)
