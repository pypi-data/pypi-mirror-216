from aniya.decorators import default, replace
from aniya.utils.undefined import undefined


@default('a', 1)
def default_value(a, b):
    return a, b


@default('a', 2, null_values=[1])
def default_replace_value(a, b):
    return a, b


@replace('a', [1, 4], 2)
def replace_value(a, b):
    return a, b


def test_default_decorator():
    # default value
    a, b = default_value(None, 2)
    assert a == 1
    assert b == 2
    a, b = default_value(undefined, 2)
    assert a == 1
    assert b == 2

    # replace value
    a, b = default_replace_value(1, 2)
    assert a == 2
    assert b == 2
    a, b = replace_value(4, 2)
    assert a == 2
    assert b == 2
