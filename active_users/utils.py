import re
from . import settings


def user_in_blacklist(username):
    return username in settings.user_blacklist()


def urls_in_blacklist(url):
    for pattern in settings.urls_blacklist():
        compiled_pattern = re.compile(pattern)
        if compiled_pattern.match(url):
            return True
    return False
