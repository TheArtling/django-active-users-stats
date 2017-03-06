"""Queries for the active_users app."""
from django.contrib.auth.models import User
from decimal import Decimal, localcontext

from dateutil.relativedelta import relativedelta

from .models import Activity
from query_utils import (
    get_months_range, parse_date, safe_div, stagger_tuple,
    get_first_last_day_of_month
)


def get_dau_for_period(start_date, end_date):
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    date_diff = end_date - start_date
    day_qs = Activity.objects.all()
    day_qs = day_qs.filter(day__range=(start_date, end_date))
    with localcontext() as ctx:
        ctx.prec = 4
        average = safe_div(Decimal(day_qs.count()), date_diff.days + 1)
    return average


def get_mau_for_period(start_date, end_date):
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    month_qs = Activity.objects.all()
    month_qs = month_qs.filter(day__range=(start_date, end_date))
    month_qs = month_qs.values_list('user__id', flat=True).distinct()
    return month_qs.count()


def get_stickiness_for_period(start_date, end_date):
    dau = get_dau_for_period(start_date, end_date)
    mau = get_mau_for_period(start_date, end_date)
    with localcontext() as ctx:
        ctx.prec = 4
        result = safe_div(dau, mau, default=0)
    return result


def get_mau_per_month(start_date, end_date):
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    months = get_months_range(start_date, end_date)
    month_tuple = [
        get_first_last_day_of_month(month.year, month.month)
        for month in months
    ]
    return [get_mau_for_period(start, end) for start, end in month_tuple]


def get_dau_per_month(start_date, end_date):
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    months = get_months_range(start_date, end_date)
    month_tuple = [
        get_first_last_day_of_month(month.year, month.month)
        for month in months
    ]
    return [get_dau_for_period(start, end) for start, end in month_tuple]


def get_stickiness_per_month(start_date, end_date, keep_day=False):
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    months = get_months_range(start_date, end_date, keep_day=keep_day)
    month_tuple = [
        get_first_last_day_of_month(month.year, month.month)
        for month in months
    ]
    return [
        get_stickiness_for_period(start, end) for start, end in month_tuple
    ]


def get_retained_users_per_month(start_date, end_date):
    """
    Returns retained users.

    Retained users are users that were active before current_month and
    during the current_month.

    Date params can be strings ('YYYY-MM-DD') or DateTime objects.

    :start_date: Start date of the time range that should be queried.
    :end_date:End date of the time range that should be queried.

    """
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    months = get_months_range(start_date, end_date)

    previous_month = start_date - relativedelta(months=1)
    months_formatted = stagger_tuple(months, previous_month)

    results = []
    for month_tuple in months_formatted:
        previous, current = month_tuple
        curr_qs = User.objects.all().filter(
            activity__day__month=current.month,
            activity__day__year=current.year)
        prev_qs = User.objects.all().filter(
            activity__day__month=previous.month,
            activity__day__year=previous.year)
        combined_qs = curr_qs & prev_qs
        combined_qs = combined_qs.distinct()
        results.append(combined_qs.count())
    return results


def get_resurrected_users_per_month(start_date, end_date):
    """
    Returns resurrected users.

    Resurrected users are users that were active in current_month but not
    active in last month.

    Date params can be strings ('YYYY-MM-DD') or DateTime objects.

    :start_date: Start date of the time range that should be queried.
    :end_date:End date of the time range that should be queried.

    """
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    months = get_months_range(start_date, end_date)
    one_month_ago = relativedelta(months=1)

    results = []
    for month in months:  # JAN
        last_month = month - one_month_ago  # DEC
        qs = User.objects.all().filter(  # ACTIVE BEFORE NOV
            activity__day__month__lte=last_month.month,
            activity__day__year__lte=last_month.year)
        qs = qs.filter(  # ACTIVE JAN
            activity__day__month=month.month,
            activity__day__year=month.year)
        qs = qs.exclude(  # ACTIVE DEC
            activity__day__month=last_month.month,
            activity__day__year=last_month.year)
        qs = qs.distinct()
        results.append(qs.count())
    return results


def get_churned_users_per_month(start_date, end_date):
    """
    Returns churned users.

    Churned users are users that were active before current_month but wasn't
    active during current_month.

    Date params can be strings ('YYYY-MM-DD') or DateTime objects.

    :start_date: Start date of the time range that should be queried.
    :end_date:End date of the time range that should be queried.

    """
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    months = get_months_range(start_date, end_date)
    one_month_ago = relativedelta(months=1)

    results = []
    for month in months:
        previous_month = month - one_month_ago
        qs = User.objects.all().filter(
            activity__day__month=previous_month.month,
            activity__day__year=previous_month.year)
        qs = qs.exclude(
            activity__day__month=month.month,
            activity__day__year=month.year)
        qs = qs.distinct()
        results.append(qs.count())
    return results
