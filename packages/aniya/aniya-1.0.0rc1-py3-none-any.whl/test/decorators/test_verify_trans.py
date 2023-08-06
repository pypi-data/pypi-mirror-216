from datetime import datetime

from aniya.decorators import trans
from aniya.utils.tpc import Date, DateTime, UnDate, UnDateTime


@trans('a', str)
def trans_string_value(a):
    return a


@trans('a', str, multi=True)
def trans_string_multi_value(a):
    return a


@trans('a', Date)
def trans_date_value(a):
    return a


@trans('a', DateTime)
def trans_datetime_value(a):
    return a


@trans('a', UnDate)
def trans_un_date_value(a):
    return a


@trans('a', UnDateTime)
def trans_un_datetime_value(a):
    return a


def test_required_decorator():
    # str
    assert trans_string_value(1) == '1'

    # date
    day = datetime(year=1998, month=8, day=23)
    assert trans_date_value('1998-08-23') == day
    assert trans_un_date_value(day) == '1998-08-23'
    assert trans_datetime_value('1998-08-23 00:00:00') == day
    assert trans_un_datetime_value(day) == '1998-08-23 00:00:00'

    # 多个值转化类型
    assert trans_string_multi_value([1, 2, 3]) == ['1', '2', '3']
