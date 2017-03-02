"""Queries for the active_users app."""
from django.contrib.auth.models import User

from dateutil.relativedelta import relativedelta

from query_utils import get_months_range, parse_date


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
    months_formatted = []
    for month in months:
        months_formatted.append(
            (previous_month, month)
        )
        previous_month = month

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
