"""Tests for the middlewares of the active users app."""
from django.test import TestCase, RequestFactory
from mixer.backend.django import mixer

from .. import middleware


class UpdateRequestsMiddlewareTestCase(TestCase):
    longMessage = True

    def test_middleware(self):
        user = mixer.blend('auth.User')
        req = RequestFactory().get('/')
        req.user = user
        req.session = {}

        middleware.GetRefererMiddleware().process_request(req)
        self.assertTrue(user.requests, msg=(
            'Should create a single entry '))
        self.assertEqual(user.requests.get_current().count(), 1, msg=(
            'Should update the current request count'))

        middleware.GetRefererMiddleware().process_request(req)
        self.assertEqual(user.requests.get_current().count(), 2, msg=(
            'Should update the current request count'))
