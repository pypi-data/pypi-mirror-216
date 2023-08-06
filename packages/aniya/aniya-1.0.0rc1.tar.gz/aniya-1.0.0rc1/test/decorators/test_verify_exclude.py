from aniya.decorators import exclude
from aniya.err import VerifyError


@exclude('a', [1, 2, 3])
def exclude_value(a):
    return a


@exclude('a', [1, 2, 3], multi=True)
def exclude_multi_value(a):
    return a


def test_exclude_decorator():
    # 单值
    assert exclude_value(4) == 4

    # 单值出现范围内值
    try:
        exclude_value(3)
    except VerifyError:
        pass

    # 多值
    assert exclude_multi_value([4, 5, 6]) == [4, 5, 6]

    # 多值出现范围内的值
    try:
        exclude_multi_value([1, 2, 3])
    except VerifyError:
        pass
