from aniya.decorators.base import combine_param
from aniya.utils.undefined import undefined


def default(key: str, default_value, null_values=(None, undefined)):
    """
    默认值
    默认值方法也可以理解为replace，只要所属值在null_values参数中，也可以做到替换某个值的作用
    :param key: 字符串key
    :param default_value: 默认值
    :param null_values: 空值列表
    """

    def middle(func):
        def inner(*args, **kwargs):
            params = combine_param(func, *args, **kwargs)
            params = _default(params, key, default_value, null_values)
            result = func(**params)
            return result

        return inner

    return middle


def replace(key: str, sources, to):
    return default(key, to, sources)


def _default(params, key, default_value, null_values=(None, undefined)):
    value = params.get(key, undefined)
    if value in null_values:
        params[key] = default_value
    return params
