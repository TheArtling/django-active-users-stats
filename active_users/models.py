"""Models for the active_users app."""
from django.db import models
from django.utils.timezone import now


class ActivityManager(models.Manager):
    def increment_date(self, user, date):
        activity, created = Activity.objects.get_or_create(
            user=user,
            day=date,
            defaults={'day': date}
        )
        if not created:
            activity.count += 1
            activity.save()
        return activity

    def increment_now(self, user):
        day = now().date()
        import ipdb; ipdb.set_trace()
        return self.increment_date(user, day)


class Activity(models.Model):
    day = models.DateField()
    count = models.IntegerField(default=1)
    user = models.ForeignKey(
        'auth.User', related_name='activity')

    objects = ActivityManager()
