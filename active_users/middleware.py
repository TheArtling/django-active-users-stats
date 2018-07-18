"""Middleware classes for the active_users app."""
from django.utils.deprecation import MiddlewareMixin

from .utils import is_blacklisted
from .models import Activity


class ActiveUsersMiddleware(MiddlewareMixin):
    """Tracks activity of users (count of actions per day)."""
    def process_request(self, request):
        if request.user.is_authenticated and not is_blacklisted(request):
            Activity.objects.increment_now(user=request.user)
