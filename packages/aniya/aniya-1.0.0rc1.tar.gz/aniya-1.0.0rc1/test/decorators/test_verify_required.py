from aniya.decorators import required
from aniya.err import VerifyError


@required('a')
def required_value(a):
    return a


def test_required_decorator():
    # 空值
    try:
        required_value(None)
    except VerifyError:
        pass
