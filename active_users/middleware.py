"""Middleware classes for the active_users app."""
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
            Activity.objects.increment_now(user=request.user)
