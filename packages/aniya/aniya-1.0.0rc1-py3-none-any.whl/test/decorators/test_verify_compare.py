from aniya.decorators import compare
from aniya.err import VerifyError


@compare('a', gt=10)
def gt_value(a):
    return a


@compare('a', gt=10, multi=True)
def gt_multi_value(a):
    return a


@compare('a', gte=10)
def gte_value(a):
    return a


@compare('a', gte=10, multi=True)
def gte_multi_value(a):
    return a


@compare('a', lt=10)
def lt_value(a):
    return a


@compare('a', lt=10, multi=True)
def lt_multi_value(a):
    return a


@compare('a', lte=10)
def lte_value(a):
    return a


@compare('a', lte=10, multi=True)
def lte_multi_value(a):
    return a


def test_compare_decorator():
    # 单值
    assert gt_value(11) > 10
    assert gte_value(10) >= 10
    assert lt_value(9) < 10
    assert lte_value(10) <= 10

    # 单值大小不对
    try:
        gt_value(10)
    except VerifyError:
        pass
    try:
        gte_value(9)
    except VerifyError:
        pass
    try:
        lt_value(10)
    except VerifyError:
        pass
    try:
        lte_value(11)
    except VerifyError:
        pass

    # 多值
    for v in gt_multi_value([11, 12, 13]):
        assert v > 10
    for v in gte_multi_value([10, 11, 12]):
        assert v >= 10
    for v in lt_multi_value([7, 8, 8]):
        assert v < 10
    for v in lte_multi_value([8, 9, 10]):
        assert v <= 10

    # 多值没有传递多个
    try:
        gt_multi_value(10)
    except VerifyError:
        pass

    # 多值大小不对
    try:
        gt_multi_value([8, 9, 10])
    except VerifyError:
        pass
    try:
        gte_multi_value([7, 8, 9])
    except VerifyError:
        pass
    try:
        lt_multi_value([10, 11, 12])
    except VerifyError:
        pass
    try:
        lte_multi_value([10, 12, 13])
    except VerifyError:
        pass
