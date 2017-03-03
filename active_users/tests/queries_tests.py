"""Tests for the queries of the active_users app."""
from decimal import Decimal, localcontext
from django.test import TestCase

from mixer.backend.django import mixer

from .. import queries, query_utils


class GetRetainedUsersPerMonthTestCase(TestCase):
    longMessage = True
    start_date = '2016-01-01'
    end_date = '2016-03-01'

    def setUp(self):
        blend = mixer.blend

        # These should be counted:
        # ----------------------------
        user = blend('auth.User')
        # Was retained in JAN, FEB and MAR
        blend('active_users.Activity', user=user, day='2015-12-01')
        blend('active_users.Activity', user=user, day='2016-01-01')
        blend('active_users.Activity', user=user, day='2016-02-01')
        blend('active_users.Activity', user=user, day='2016-03-01')

        user = blend('auth.User')
        # Was only retained in JAN
        blend('active_users.Activity', user=user, day='2015-12-01')
        blend('active_users.Activity', user=user, day='2016-01-01')

        # These should NOT be counted:
        # ----------------------------
        # User before time range
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2015-11-01')
        blend('active_users.Activity', user=user, day='2015-12-01')

        # User after time range
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2016-03-01')
        blend('active_users.Activity', user=user, day='2016-04-01')

        # User who is not retained but churned
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2015-12-01')

        # User who is not retained but recovered
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2015-11-01')
        blend('active_users.Activity', user=user, day='2016-01-01')

    def test_query(self):
        result = queries.get_retained_users_per_month(
            self.start_date, self.end_date)
        self.assertEqual(result, [2, 1, 1])


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
        blend('active_users.Activity', user=user, day='2016-01-01')

        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2015-10-01')
        blend('active_users.Activity', user=user, day='2016-01-01')

        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2016-01-01')
        blend('active_users.Activity', user=user, day='2016-03-01')

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
        blend('active_users.Activity', user=user, day='2016-01-01')
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


class GetBaseAverageTestCase(TestCase):
    longMessage = True
    start_date = '2016-01-01T00:00:00+00:00'
    end_date = '2016-03-01T00:00:00+00:00'

    def setUp(self):
        blend = mixer.blend
        # User 1
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2016-01-01')
        blend('active_users.Activity', user=user, day='2016-01-02')
        blend('active_users.Activity', user=user, day='2016-01-03')

        blend('active_users.Activity', user=user, day='2016-02-01')
        blend('active_users.Activity', user=user, day='2016-02-02')
        blend('active_users.Activity', user=user, day='2016-02-03')

        blend('active_users.Activity', user=user, day='2016-03-01')
        blend('active_users.Activity', user=user, day='2016-03-02')
        blend('active_users.Activity', user=user, day='2016-03-03')

        # User 2
        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2016-01-01')
        blend('active_users.Activity', user=user, day='2016-01-02')
        blend('active_users.Activity', user=user, day='2016-01-03')

        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2016-02-01')
        blend('active_users.Activity', user=user, day='2016-02-02')
        blend('active_users.Activity', user=user, day='2016-02-03')

        user = blend('auth.User')
        blend('active_users.Activity', user=user, day='2016-03-01')
        blend('active_users.Activity', user=user, day='2016-03-02')
        blend('active_users.Activity', user=user, day='2016-03-03')


class GetDAUAverageTestCase(GetBaseAverageTestCase):

    def test_for_period(self):
        start, end = query_utils.get_first_last_day_of_month(2016, 1)
        result = queries.get_dau_for_period(start, end)
        with localcontext() as ctx:
            ctx.prec = 4
            expected = Decimal('.1935')
        self.assertEqual(result, expected)

        end = end.replace(day=3)
        result = queries.get_dau_for_period(start, end)
        self.assertEqual(result, 2)

    def test_for_month(self):
        start = '2016-01-01T00:00:00+00:00'
        end = '2016-03-03T00:00:00+00:00'
        result = queries.get_dau_per_month(start, end)
        with localcontext() as ctx:
            ctx.prec = 4
            expected = [
                Decimal(6)/31,
                Decimal(6)/29,
                Decimal(6)/31
            ]
        self.assertEqual(result, expected)


class GetMAUTestCase(GetBaseAverageTestCase):

    def test_for_period(self):
        start, end = query_utils.get_first_last_day_of_month(2016, 1)
        result = queries.get_mau_for_period(start, end)
        Decimal(.1935)
        self.assertEqual(result, Decimal(2))

    def test_for_month(self):
        start = '2016-01-01T00:00:00+00:00'
        end = '2016-03-03T00:00:00+00:00'
        result = queries.get_mau_per_month(start, end)
        expected = [Decimal(2), Decimal(2), Decimal(2)]
        self.assertEqual(result, expected)


class GetStickinessTestCase(GetBaseAverageTestCase):

    def test_for_period(self):
        start, end = query_utils.get_first_last_day_of_month(2016, 1)
        result = queries.get_stickiness_for_period(start, end)
        with localcontext() as ctx:
            ctx.prec = 4
            self.assertEqual(result, Decimal(6)/31/2)

    def test_for_month(self):
        start = '2016-01-01T00:00:00+00:00'
        end = '2016-03-03T00:00:00+00:00'
        result = queries.get_stickiness_per_month(start, end)
        with localcontext() as ctx:
            ctx.prec = 4
            expected = [
                Decimal(6)/31/2,
                Decimal(6)/29/2,
                Decimal(6)/31/2
            ]
        self.assertEqual(result, expected)
