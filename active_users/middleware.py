"""Middleware classes for the active_users app."""
from django.utils.timezone import now

from .utils import is_blacklisted
from .models import Activity


class ActiveUsersMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

    def process_request(self, request):
        if request.user.is_authenticated() and not is_blacklisted(request):
            day = now().date()
            activity, created = Activity.objects.get_or_create(
                user=request.user,
                day=day,
                defaults={'day': day}
            )
            if not created:
                activity.count += 1
                activity.save()
