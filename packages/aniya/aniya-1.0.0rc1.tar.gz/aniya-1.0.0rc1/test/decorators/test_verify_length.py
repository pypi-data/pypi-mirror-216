from aniya.decorators import length
from aniya.err import VerifyError


@length('a', min_length=10, max_length=20)
def length_value(a):
    return len(a)


@length('a', min_length=10, max_length=20, multi=True)
def length_multi_value(a):
    return [len(item) for item in a]


def test_length_decorator():
    # 单值
    assert length_value('1234567890') == 10

    # 无法获取长度的数据类型
    try:
        length_value(11) == 10  # noqa
    except VerifyError:
        pass

    # 不再长度范围之内
    try:
        length_value('12345678')
    except VerifyError:
        pass

    # 多值
    assert length_multi_value(['1234567890', '12345678901']) == [10, 11]

    # 多值中出现无法获取长度
    try:
        length_multi_value(['1234567890', 12345678901])
    except VerifyError:
        pass

    # 多值中出现不在长度范围之内
    try:
        length_multi_value(['123456', '12345678901'])
    except VerifyError:
        pass
