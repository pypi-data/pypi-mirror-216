import dataclasses
import json
from typing import Any

from aniya import g


@dataclasses.dataclass
class PanicFmtData:
    key: str
    assign: Any = None
    value: Any = None


class VerifyError(ValueError):
    """ 
    当验证失败时，统一使用的异常报错类
    """

    def __init__(self, error_key: str, fmt_data: PanicFmtData) -> None:
        self.key = error_key
        self._fmt_data = fmt_data
        self.error = g.err_msg.get(error_key) % fmt_data.__dict__
        super().__init__()

    def json(self):
        """
        异常结果转化为json
        """
        return json.dumps(self.dict())

    def dict(self):
        """
        异常结果转化为python的字典
        """
        return {self.key: self.error}

    def string(self):
        """
        异常结果转化为字符串
        """
        return self.error

    def __str__(self):
        return self.string()

    def __repr_args__(self):
        return self.string()
