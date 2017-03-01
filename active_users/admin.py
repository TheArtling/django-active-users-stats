"""Admin classes for the active_users app."""
from django.contrib import admin

from . import models


class ActivityAdmin(admin.ModelAdmin):
    list_display = ['day', 'count', 'user']


admin.site.register(models.Activity, ActivityAdmin)
