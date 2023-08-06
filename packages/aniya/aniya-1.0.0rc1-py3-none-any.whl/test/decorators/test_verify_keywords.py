from aniya.decorators import include_keys, exclude_keys
from aniya.err import VerifyError


@include_keys('a', {'name', 'age'})
def include_keys_value(a):
    return a


@exclude_keys('a', {'name', 'age'})
def exclude_keys_value(a):
    return a


def test_include_keys_decorator():
    data = {'name': 'aniya', 'age': 6, 'gender': '女'}
    assert include_keys_value(data) == data

    data = {'username': 'aniya', 'password': 'aniya'}
    try:
        include_keys_value(data)
    except VerifyError:
        pass


def test_exclude_keys_decorator():
    data = {'username': 'aniya', 'password': 'aniya'}
    assert exclude_keys_value(data) == data

    data = {'name': 'aniya', 'age': 6, 'gender': '女'}
    try:
        exclude_keys_value(data)
    except VerifyError:
        pass
