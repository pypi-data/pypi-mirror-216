def combine_param(func, *args, **kwargs) -> dict:
    """
    在装饰器中，合并 *args 和 **kwargs 两个参数
    """
    return {**dict(zip(func.__code__.co_varnames, args)), **kwargs}
