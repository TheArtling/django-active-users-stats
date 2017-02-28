"""Tests for the middlewares of the active_users app."""
from django.test import TestCase, RequestFactory

from mixer.backend.django import mixer

from .. import middleware


class ActiveUsersMiddlewareTestCase(TestCase):
    longMessage = True

    def test_middleware(self):
        user = mixer.blend('auth.User')
        req = RequestFactory().get('/')
        req.user = user

        middleware.ActiveUsersMiddleware().process_request(req)
        self.assertEquals(user.activity.all().count(), 1, msg=(
            'Should create an activity object for current day'))

        middleware.ActiveUsersMiddleware().process_request(req)
        self.assertEqual(user.activity.all().count(), 1, msg=(
            'Should create update the existing activity object for current'
            ' day'))

        obj = user.activity.all().first()
        self.assertEqual(obj.count, 2, msg=(
            'When the user has made two requests, the count should be 2'))

        # TODO somehow use hasattr and check for is_impersonated (is that the=
        # attribute name?) and ignore those requests
