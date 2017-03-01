"""Tests for the queries of the active_users app."""
from datetime import date

from django.test import TestCase

from mixer.backend.django import mixer

from .. import queries


class GetRetainedUsersPerMonth(TestCase):
    longMessage = True
    start_date = '2016-01-01'
    end_date = '2016-03-01'

    def setUp(self):
        blend = mixer.blend

        # These should be counted:
        # ----------------------------
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day=date(2015, 12, 1))
        blend('active_users.Activity', user=user, day=self.start_date)
        blend('active_users.Activity', user=user, day=date(2016, 2, 1))
        blend('active_users.Activity', user=user, day=self.end_date)

        user = blend('auth.User')
        blend('active_users.Activity', user=user, day=date(2015, 12, 1))
        blend('active_users.Activity', user=user, day=self.start_date)

        # These should NOT be counted:
        # ----------------------------
        # User before time range (will be counted in cumulative)
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day=date(2015, 11, 1))
        blend('active_users.Activity', user=user, day=date(2015, 12, 1))

        # User after time range
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day=date(2016, 3, 1))
        blend('active_users.Activity', user=user, day=date(2016, 4, 1))

        # User who is not retained but churned
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day=date(2015, 12, 1))

        # User who is not retained but recovered or new
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day=date(2016, 1, 1))

    def test_query(self):
        result = queries.get_retained_users_per_month(
            self.start_date, self.end_date)
        self.assertEqual(set(result), set([2, 1, 1]))


class GetResurrectedUsersPerMonth(TestCase):
    longMessage = True
    start_date = '2016-01-01'
    end_date = '2016-03-01'

    def setUp(self):
        blend = mixer.blend
        # These should be counted:
        # ------------------------
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2015-11-01')
        blend('active_users.Activity', user=user, day=self.start_date)

        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2015-10-01')
        blend('active_users.Activity', user=user, day=self.start_date)

        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2016-01-01')
        blend('active_users.Activity', user=user, day=self.end_date)

        # These should not be counted:
        # ----------------------------
        # User before time range
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2015-10-01')
        blend('active_users.Activity', user=user, day='2015-12-01')

        # User after time range
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2016-02-01')
        blend('active_users.Activity', user=user, day='2016-04-01')

        # User who is retained
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2016-01-01')
        blend('active_users.Activity', user=user, day='2016-02-01')

        # User who only has one activity
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2016-02-01')

        # User who is active
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2016-01-01')
        blend('active_users.Activity', user=user, day='2016-02-01')
        blend('active_users.Activity', user=user, day='2016-03-01')

    def test_query(self):
        result = queries.get_resurrected_users_per_month(
            self.start_date, self.end_date)
        self.assertEqual(set(result), set([2, 0, 1]))


class GetChurnedUsersPerMonth(object):
    longMessage = True

    def test_query(self):
        user = mixer.blend('auth.User')
        mixer.blend('active_users.Activity', user=user, day='2016-01-0')

        # Time range shall be JAN - MAR
        start_date = '2016-01-01'
        end_date = '2016-03-31'

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

        queries.get_churned_users_per_month(start_date, end_date)
        # should be [2, 0, 1]
