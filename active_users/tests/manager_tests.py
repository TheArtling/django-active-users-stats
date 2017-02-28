"""Tests for the managers of the active_users app."""
from django.test import TestCase
from django.utils.timezone import now, timedelta

from freezegun import freeze_time

from mixer.backend.django import mixer

from ..models import Activity


class ActivityManagerTestCase(TestCase):
    longMessage = True

    def test_get_current(self):
        user = mixer.blend('auth.User')

        yesterday = now() - timedelta(days=1)
        # We create an instance for yesterday, this should NOT be returned
        yesterday_obj = mixer.blend(
            'active_users.Activity', user=user, day=yesterday.date())

        with freeze_time("2012-01-14"):
            now_obj = Activity.objects.increment_now(user)
            self.assertTrue(now_obj, msg=(
                'Should return newly create Activity instance for the current'
                ' day'))
            self.assertNotEqual(yesterday_obj.pk, now_obj.pk, msg=(
                'now obj should not be the same as yesterday_obj'))

            now_obj2 = Activity.objects.increment_now(user)
            self.assertEqual(now_obj2.pk, now_obj.pk, msg=(
                'Should return the instance for the current day'))
            self.assertEqual(now_obj2.count, 2, msg=(
                'Should return the instance for the current day'))
