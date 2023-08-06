from datetime import datetime


class DateTime:
    """
    日期fmt的方式改为类实例化的方式返回datetime类型的值
    format: %Y-%m-%d %H%M%S
    """
    _format = '%Y-%m-%d %H:%M:%S'

    def __init__(self, dt: str):
        self.dt = dt

    def __new__(cls, *args, **kwargs):
        params = dict(zip(cls.__init__.__code__.co_varnames[1:], args))
        dt = params['dt']
        instance = datetime.strptime(dt, cls._format)
        return instance


class Date:
    """
    日期fmt的方式改为类实例化的方式返回datetime类型的值
    format: %Y-%m-%d
    """
    _format = '%Y-%m-%d'

    def __init__(self, dt: str):
        self.dt = dt

    def __new__(cls, *args, **kwargs):
        params = dict(zip(cls.__init__.__code__.co_varnames[1:], args))
        dt = params['dt']
        instance = datetime.strptime(dt, cls._format)
        return instance


class UnDateTime:
    """
    将日期格式数据转化为字符串
    format: %Y-%m-%d
    """
    _format = '%Y-%m-%d %H:%M:%S'

    def __init__(self, dt):
        self.dt = dt

    def __new__(cls, *args, **kwargs):
        params = dict(zip(cls.__init__.__code__.co_varnames[1:], args))
        dt = params['dt']
        instance = dt.strftime(cls._format)
        return instance


class UnDate:
    """
    将日期格式数据转化为字符串
    format: %Y-%m-%d
    """
    _format = '%Y-%m-%d'

    def __init__(self, dt):
        self.dt = dt

    def __new__(cls, *args, **kwargs):
        params = dict(zip(cls.__init__.__code__.co_varnames[1:], args))
        dt = params['dt']
        instance = dt.strftime(cls._format)
        return instance
