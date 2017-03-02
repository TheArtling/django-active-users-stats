"""Tests for the models of the active_users app."""
from django.test import TestCase
from django.utils.timezone import now

from freezegun import freeze_time
from mixer.backend.django import mixer

from ..models import Activity


class ActivityManagerTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.user = mixer.blend('auth.User')

    def test_increment_date(self):
        with freeze_time('1900-01-01'):
            today = now()
            r1 = Activity.objects.increment_date(self.user, today)
            self.assertEqual(r1.count, 1, msg=(
                'Should create new Activity instance with default count = 1'))

            r2 = Activity.objects.increment_date(self.user, today)
            self.assertTrue(r2.count, msg=(
                'Should increase count on existing instance'))

    def test_increment_now(self):
        with freeze_time('1900-01-01'):
            today = now().date()
            r1 = Activity.objects.increment_now(self.user)
            self.assertEqual(r1.day, today, msg=(
                'Should create an instance for the current day'))
            r2 = Activity.objects.increment_now(self.user)
            self.assertEqual(r2.count, 2, msg=(
                'Should increase count on existing instance'))


class ActivityTestCase(TestCase):
    # TODO: copy and paste!
    """Tests for the ``Favorite`` model."""
    longMessage = True

    def test_model(self):
        user = mixer.blend('auth.User')
        obj = mixer.blend('active_users.Activity', user=user)
        self.assertTrue(obj.pk, msg=('Should save an instance.'))
