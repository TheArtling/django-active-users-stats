"""Queries for the active_users app."""
from django.contrib.auth.models import User

from dateutil.relativedelta import relativedelta

from query_utils import get_months_range, parse_date


def get_retained_users_per_month(start_date, end_date):
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    months = get_months_range(start_date, end_date)

    previous_month = start_date - relativedelta(months=1)
    months_formatted = []
    for month in months:
        if previous_month:
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
        curr_id = list(curr_qs.values_list('pk', flat=True))
        prev_qs = User.objects.all().filter(
            activity__day__month=previous.month,
            activity__day__year=previous.year)
        prev_id = list(prev_qs.values_list('pk', flat=True))
        results.append(len(set(curr_id).intersection(prev_id)))
    return results
