"""Tests for the queries of the active_users app."""
from datetime import date

from django.test import TestCase

from mixer.backend.django import mixer

from .. import queries


class GetRetainedUsersPerMonthTestCase(TestCase):
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


class GetResurrectedUsersPerMonthTestCase(TestCase):
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

        # User who is new
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


class GetChurnedUsersPerMonthTestCase(TestCase):
    longMessage = True
    start_date = '2016-01-01'
    end_date = '2016-03-01'

    def setUp(self):
        blend = mixer.blend
        # These should be counted:
        # ------------------------

        # User1 churned in JAN
        # create Activity in NOV
        # create Activity in DEC
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2015-11-01')
        blend('active_users.Activity', user=user, day='2015-12-01')

        # User2 churned in JAN
        # create Activity in NOV
        # create Activity in DEC
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2015-11-01')
        blend('active_users.Activity', user=user, day='2015-12-01')

        # User3 churned in MAR
        # create Activity in JAN
        # create Activity in FEB
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day=self.start_date)
        blend('active_users.Activity', user=user, day='2016-02-01')

        # These should not be counted:
        # ----------------------------

        # User after time range
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2016-04-01')
        blend('active_users.Activity', user=user, day='2016-05-01')

        # User who is active
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2016-01-01')
        blend('active_users.Activity', user=user, day='2016-02-01')
        blend('active_users.Activity', user=user, day='2016-03-01')

    def test_query(self):
        result = queries.get_churned_users_per_month(
            self.start_date, self.end_date)
        self.assertEqual(set(result), set([2, 0, 1]))
