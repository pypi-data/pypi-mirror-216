from decimal import Decimal
from aniya.decorators import digits
from aniya.err import VerifyError


@digits('a', decimals=2)
def digits_number(a):
    return str(a)


@digits('a', decimals=2, multi=True)
def digits_multi_number(a):
    return str(a)


def test_digits_decorator():
    # 单值
    assert digits_number(10) == '10'
    assert digits_number(10.00) == '10.0'
    assert digits_number(10.0101) == '10.01'
    assert digits_number(Decimal('10.0202')) == '10.02'

    # 多值
    assert digits_multi_number([8, 9.0, 10.01, 11.0101, 12.020202, 13.030303]) == '[8, 9.0, 10.01, 11.01, 12.02, 13.03]'

    # 错误类型
    try:
        digits_number('10')
    except VerifyError:
        pass

    # 未传递多个
    try:
        digits_multi_number(10)
    except VerifyError:
        pass
