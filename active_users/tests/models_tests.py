"""Tests for the models of the active_users app."""
from django.test import TestCase
from mixer.backend.django import mixer


class ActiveUserTestCase(TestCase):
    """Tests for the ``Favorite`` model."""
    def test_model(self):
        user = mixer.blend('auth.User')
        obj = mixer.blend('active_users.ActiveUser', user=user)
        self.assertTrue(obj.pk, msg=('Should save an instance.'))
