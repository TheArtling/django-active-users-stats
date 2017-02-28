import re
from . import settings


def user_in_blacklist(username):
    return username in settings.user_blacklist()


def urls_in_blacklist(url):
    for pattern in settings.urls_blacklist():
        if pattern == '':
            continue
        compiled_pattern = re.compile(pattern)
        if compiled_pattern.match(url):
            return True
    return False


def is_blacklisted(request):
    return (request.user.is_superuser or
            user_in_blacklist(request.user.username) or
            urls_in_blacklist(request.path))
