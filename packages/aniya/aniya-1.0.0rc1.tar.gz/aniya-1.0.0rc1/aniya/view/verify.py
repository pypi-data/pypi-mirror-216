"""
要检查的参数被传入，如果在验证后检查失败，则相关将抛出异常。这种方法指的是pydantic的形式，
但区别在于返回的结果可以自定义。

e.g.:
    from aniya.view import BaseView

    class Param(BaseModel):
        username:
        password: str

    data = {'username': 'demo', 'password': '88888888'}
    verify_data = Param(**data)
"""
from aniya.err import VerifyError


class BaseModel:
    """
    由class定义的模型验证规则的基类，只有具有单层参数结构的类才会被解析。
    """

    def __init__(self, **data) -> None:
        self._verify_data: dict = data
        self._error_cls = VerifyError

    def _context(self):
        """ 
        参数验证的执行过程。
        """

    def _get_cls_property(self):
        ...


class BaseDepModel:
    """
    一个可以解析复杂嵌套结构数据的类。
    """
