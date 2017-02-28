"""Models for the active_users app."""
from django.db import models


class Activity(models.Model):
    day = models.DateField()
    count = models.IntegerField(default=1)
    user = models.ForeignKey(
        'auth.User', related_name='activity')
