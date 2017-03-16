"""Tests for the models of the active_users app."""
from django.test import TestCase
from django.utils.timezone import now
from django.db import IntegrityError

from freezegun import freeze_time
from mixer.backend.django import mixer

from ..models import Activity

@freeze_time('1900-01-01')
class ActivityManagerTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.user = mixer.blend('auth.User')

    def test_increment_date(self):
        today = now()
        r1 = Activity.objects.increment_date(self.user, today)
        self.assertEqual(r1.count, 1, msg=(
            'Should create new Activity instance with default count = 1'))

        r2 = Activity.objects.increment_date(self.user, today)
        self.assertTrue(r2.count, msg=(
            'Should increase count on existing instance'))

    def test_increment_now(self):
        today = now().date()
        r1 = Activity.objects.increment_now(self.user)
        self.assertEqual(r1.day, today, msg=(
            'Should create an instance for the current day'))
        r2 = Activity.objects.increment_now(self.user)
        self.assertEqual(r2.count, 2, msg=(
            'Should increase count on existing instance'))


class ActivityTestCase(TestCase):
    """Tests for the ``Activity`` model."""
    longMessage = True

    def setUp(self):
        self.user = mixer.blend('auth.User')

    def test_model(self):
        user = mixer.blend('auth.User')
        obj = mixer.blend('active_users.Activity', user=user)
        self.assertTrue(obj.pk, msg=('Should save an instance.'))

    def test_unique(self):
        with freeze_time('1900-01-01'):
            today = now()
            mixer.blend('active_users.Activity', user=self.user, day=today)
            self.assertRaises(
                IntegrityError, mixer.blend,
                'active_users.Activity', user=self.user, day=today,
                msg=('Should throw an integrity error when the same user and'
                     ' day is made'))
