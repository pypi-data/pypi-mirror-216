from aniya.err import VerifyError, PanicFmtData


class Undefined:  # noqa

    def __repr__(self) -> str:
        return 'aniya undefined'

    def __copy__(self):
        return self


undefined = Undefined()


def check_undefined(params, key):
    """
    检查返回值是不是undefined
    """
    value = params.get(key, undefined)
    if isinstance(value, Undefined):
        raise VerifyError('undefined', PanicFmtData(key, None, value))
    return value
