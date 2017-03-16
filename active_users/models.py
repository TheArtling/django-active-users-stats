"""Models for the active_users app."""
from django.db import models
from django.utils.timezone import now


class ActivityManager(models.Manager):
    def increment_date(self, user, date):
        """Increments the Action instance for the given user and date."""
        activity, created = self.get_or_create(
            user=user,
            day=date,
            defaults={'day': date}
        )
        if not created:
            activity.count += 1
            activity.save()
        return activity

    def increment_now(self, user):
        """
        Increments the Action instance for the given user and the current day.

        Convenience wrapper around `increment_date`.

        """
        day = now().date()
        return self.increment_date(user, day)


class Activity(models.Model):
    day = models.DateField()
    last_active = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=1)
    user = models.ForeignKey(
        'auth.User', related_name='activity')

    objects = ActivityManager()

    class Meta:
        unique_together = ("day", "user")
