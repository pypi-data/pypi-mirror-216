from aniya.decorators import include
from aniya.err import VerifyError


@include('a', [1, 2, 3])
def include_value(a):
    return a


@include('a', [1, 2, 3], multi=True)
def include_multi_value(a):
    return a


def test_include_decorator():
    # 单值
    assert include_value(3) == 3

    # 单值未出现范围内值
    try:
        include_value(4)
    except VerifyError:
        pass

    # 多值
    assert include_multi_value([1, 2, 3]) == [1, 2, 3]

    # 多值未出现范围内的值
    try:
        include_multi_value([4, 5, 6])
    except VerifyError:
        pass
