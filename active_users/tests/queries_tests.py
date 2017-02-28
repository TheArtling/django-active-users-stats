"""Tests for the queries of the active_users app."""
from django.test import TestCase
from django.utils.timezone import now

from mixer.backend.django import mixer


class GetRetainedUsersPerMonth(TestCase):
    longMessage = True

    def test_query(self):
        today = now()
        user = mixer.blend('auth.User')
        mixer.blend('active_users.Activity', user=user, day='2016-01-0'

        # Time range shall be JAN - MAR

        # These should be counted:
        # ------------------------

        # User1
        # create Activity in DEC
        # create Activity in JAN

        # User2
        # create Activity in DEC
        # create Activity in JAN

        # User1
        # create Activity in FEB
        # create Activity in MAR


        # These should NOT be counted:
        # ----------------------------
        # User before time range (will be counted in cumulative)
        # create Activity in NOV
        # create Activity in DEC

        # User after time range
        # create Activity in MAR
        # create Activity in APR

        # User who is not retained but churned
        # create Activity in DEC

        # User who is not retained but recovered or new
        # create Activity in JAN

        result = queries.get_retained_users_per_month(start_date, end_date)
        # should be [2, 0, 1]


class GetRecoveredUsersPerMonth(TestCase):
    longMessage = True

    def test_query(self):
        today = now()
        user = mixer.blend('auth.User')
        mixer.blend('active_users.Activity', user=user, day='2016-01-0'

        # Time range shall be JAN - MAR

        # These should be counted:
        # ------------------------

        # User1
        # create Activity in NOV
        # create Activity in JAN

        # User2
        # create Activity in OCT
        # create Activity in JAN

        # User3
        # create Activity in JAN
        # create Activity in MAR


        # These should not be counted:
        # ----------------------------
        # User before time range
        # create Activity in OCT
        # create Activity in DEC

        # User after time range
        # create Activity in FEB
        # create Activity in APR

        # User who is retained
        # create Activity in JAN
        # create Activity in FEB

        # User who is churned or new
        # create Activity in JAN

        result = queries.get_recovered_users_per_month(start_date, end_date)
        # should be [2, 0, 1]


class GetChurnedUsersPerMonth(TestCase):
    longMessage = True

    def test_query(self):
        today = now()
        user = mixer.blend('auth.User')
        mixer.blend('active_users.Activity', user=user, day='2016-01-0'

        # Time range shall be JAN - MAR

        # These should be counted:
        # ------------------------

        # User1 churned in JAN
        # create Activity in NOV
        # create Activity in DEC

        # User2 churned in JAN
        # create Activity in NOV
        # create Activity in DEC

        # User3 churned in MAR
        # create Activity in JAN
        # create Activity in FEB


        # These should not be counted:
        # ----------------------------
        # User before time range
        # create Activity in OCT
        # create Activity in NOV

        # User after time range
        # create Activity in FEB
        # create Activity in MAR

        # User who is retained
        # create Activity in JAN
        # create Activity in FEB

        # User who is new (never did anything before)
        # create Activity in JAN

        result = queries.get_churned_users_per_month(start_date, end_date)
        # should be [2, 0, 1]
