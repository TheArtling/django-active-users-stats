"""Tests for the queries utils of the active_users app."""
import pytz
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
from django.test import TestCase

from .. import query_utils as utils


class QueryUtilsTest(TestCase):
    longMessage = True

    def test_get_month_names(self):
        test_date = date(2013, 1, 30)
        month_name = utils.get_month_name(test_date)
        self.assertEqual(month_name, 'Jan', msg=(
            'should print abbreviated month name'))

    def test_parsed_date(self):
        test_date = '2013-1-30'
        parsed_date = utils.parse_date(test_date)
        expected = datetime(2013, 1, 30, 0, 0, tzinfo=pytz.UTC)
        self.assertEqual(parsed_date, expected, msg=(
            'should parse date if string is well formed'))

        test_date = datetime(2013, 1, 30, 0, 0)
        parsed_date = utils.parse_date(test_date)
        expected = datetime(2013, 1, 30, 0, 0, tzinfo=pytz.UTC)
        self.assertEqual(parsed_date, expected, msg=(
            'should return the datetime object if test_date is a datetime'
            ' object'))

    def test_get_months_range(self):
        start_date = datetime(2016, 01, 01, 0, 0, tzinfo=pytz.UTC)
        end_date = datetime(2016, 03, 01, 0, 0, tzinfo=pytz.UTC)
        start = datetime(2016, 01, 01, 0, 0, tzinfo=pytz.UTC)
        expected = [start + relativedelta(months=i) for i in range(0, 3)]
        result = utils.get_months_range(start_date, end_date)
        self.assertEqual(set(result), set(expected))
