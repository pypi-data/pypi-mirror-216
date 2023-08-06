from aniya.decorators import callback


def add_one(value):
    return value + 1


def add_two(value):
    return value + 2


@callback('a', add_one)
def callback_value_add_one(a):
    return a


@callback('a', [add_one, add_two])
def callback_value_add_three(a):
    return a


def test_callback_decorator():
    # 0 + 1
    a = callback_value_add_one(0)
    assert a == 1

    # 0 + 1 + 2
    a = callback_value_add_three(0)
    assert a == 3
