import pytz
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse as parseDateString
from datetime import datetime


def get_month_name(month):
    return month.strftime('%b')


def get_months_range(start_date, end_date):
    """
    Returns a list of all months that are within start_date and end_date.
    Useful when we need to fill up missing months in a QuerySet where there
    were no results in that month and fill up those months with the value `0`.
    """
    months = []
    current_month = datetime(
        start_date.year,
        start_date.month,
        start_date.day,
        tzinfo=pytz.UTC)
    while current_month <= end_date:
        months.append(current_month)
        current_month = current_month + relativedelta(months=1)
    return months


def parse_date(date_val):
    type_test = (isinstance(date_val, basestring) or
                 isinstance(date_val, datetime))
    assert type_test, "Invalid arguements supplied to parse_date"

    if isinstance(date_val, basestring):
        parsed_date = parseDateString(date_val)
    else:
        parsed_date = date_val
    return parsed_date.replace(tzinfo=pytz.UTC)
