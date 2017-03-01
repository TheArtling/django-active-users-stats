from django.conf import settings


DEFAULTS = {
    'users': [''],
    'urls': ['/admin/.*']
}

BASE_SETTING_KEY = 'ACTIVE_USERS_BLACKLIST'
USER_KEY = 'users'
URLS_KEY = 'urls'


def get_blacklist(key):
    if hasattr(settings, BASE_SETTING_KEY):
        user_settings = getattr(settings, BASE_SETTING_KEY)
        return getattr(user_settings, key, [])
    else:
        return DEFAULTS[key]


def user_blacklist():
    return get_blacklist(USER_KEY)


def urls_blacklist():
    return get_blacklist(URLS_KEY)
