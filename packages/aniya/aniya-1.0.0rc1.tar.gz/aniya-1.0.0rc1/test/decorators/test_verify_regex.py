from aniya.decorators import regex
from aniya.err import VerifyError


@regex('a', r'\d+')
def regex_value(a):
    return a


@regex('a', r'\d+', multi=True)
def regex_multi_value(a):
    return a


def test_regex_decorator():
    # 单值符合正则规则
    assert regex_value('111') == '111'

    # 单值数据类型不符合
    try:
        regex_value(111)
    except VerifyError:
        pass

    # 单值不符合正则规则
    try:
        regex_value('aaa')
    except VerifyError:
        pass

    # 多值符合正则规则
    assert regex_multi_value(['111', '222']) == ['111', '222']

    # 多值不符合类型
    try:
        regex_value([111, 222])
    except VerifyError:
        pass

    # 多值不符合正则规则
    try:
        regex_value(['aaa', '222'])
    except VerifyError:
        pass
