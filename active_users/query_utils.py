import calendar
import pytz

from decimal import (
    Decimal, DivisionByZero, DivisionUndefined, InvalidOperation
)
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse as parseDateString
from datetime import datetime


def get_month_name(month):
    return month.strftime('%b')


def reset_to_first_day(date):
    return date.replace(day=1)


def get_first_last_day_of_month(year, month, tzinfo=pytz.UTC):
    _, num_days = calendar.monthrange(year, month)
    first_day = datetime(year, month, 1, tzinfo=tzinfo)
    last_day = first_day.replace(
        day=num_days, hour=23, minute=59, second=59, microsecond=999)
    return (first_day, last_day)


def safe_div(op1, op2, default=None):
    """Just a simple wrapper to catch division by zero errors."""
    try:
        return Decimal(str(op1)) / Decimal(str(op2))
    except (DivisionByZero, DivisionUndefined, InvalidOperation):
        if default:
            return default
        return 'inf'


def stagger_tuple(elements_list, initial=None):
    """
    Converts a list of objects into a staggered tuple

    Example:
    [1, 2, 3, 4, 5]
    [(1, 2), (2, 3), (3, 4), (4, 5)]

    """
    res = []
    previous_element = initial
    for element in elements_list:
        if previous_element is not None:
            res.append((previous_element, element))
        previous_element = element
    return res


def get_months_range(start_date, end_date, keep_day=False):
    """
    Returns a list of all months that are within start_date and end_date.
    Useful when we need to fill up missing months in a QuerySet where there
    were no results in that month and fill up those months with the value `0`.
    """
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)

    if not keep_day:
        start_date = reset_to_first_day(start_date)

    months = []
    while start_date <= end_date:
        months.append(start_date)
        start_date = start_date + relativedelta(months=1)
    return months


def coerce_to_UTC(date):
    if date.tzinfo is pytz.UTC:
        return date

    coerced = None
    try:
        coerced = date.astimezone(pytz.UTC)
    except (ValueError, TypeError):
        coerced = date.replace(tzinfo=pytz.utc)
    return coerced


def parse_date(date_val):
    type_test = (isinstance(date_val, basestring) or
                 isinstance(date_val, datetime))
    assert type_test, "Invalid arguements supplied to parse_date"

    if isinstance(date_val, basestring):
        parsed_date = parseDateString(date_val)
    else:
        parsed_date = date_val
    return coerce_to_UTC(parsed_date)
