"""Tests for the managers of the active_users app."""
from django.test import TestCase, RequestFactory
from django.utils.timezone import now, timedelta

from mixer.backend.django import mixer

from ..models import Activity


class ActivityManagerTestCase(TestCase):
    longMessage = True

    def test_get_current(self):
        user = mixer.blend('auth.User')
        obj = Activity.objects.get_current(user)
        self.assertFalse(obj, msg=('Should return empty queryset'))

        today = now()
        yesterday = today - timedelta(days=1)
        # We create an instance for yesterday, this should NOT be returned
        mixer.blend('active_users.Activity', user=user, day=yesterday, count=1)

        obj = Activity.objects.get_current(user)
        self.assertFalse(obj, msg=(
            'Should return empty queryset because there is no entry for the'
            ' current day, yet'))

        obj = Activity.objects.get_current(user, create=True)
        self.assertTrue(obj, msg=(
            'Should return newly create Activity instance for the current'
            ' day'))

        obj2 = Activity.objects.get_current(user)
        self.assertEqual(obj2.pk, obj.pk, msg=(
            'Should return the instance for the current day'))
