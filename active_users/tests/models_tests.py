"""Tests for the models of the active_users app."""
from django.test import TestCase

from mixer.backend.django import mixer


class ActivityTestCase(TestCase):
    """Tests for the ``Favorite`` model."""
    def test_model(self):
        user = mixer.blend('auth.User')
        obj = mixer.blend('active_users.Activity', user=user)
        self.assertTrue(obj.pk, msg=('Should save an instance.'))
