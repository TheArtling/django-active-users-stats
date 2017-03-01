"""Helper functions for the active_users app."""
from django.conf import settings


def user_in_blacklist(pk):
    """
    Returns `True` if requests for the given user.pk should not be counted.

    """
    return pk in getattr(
        settings, 'ACTIVE_USERS_USER_BLACKLIST', [])


def is_blacklisted(request):
    """Returns `True` if the request should not be counted."""
    return (request.user.is_superuser or
            request.user.is_staff or
            user_in_blacklist(request.user.username))
