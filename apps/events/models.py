from django.conf import settings
from django.db import models
from django.utils import timezone


class EventQuerySet(models.QuerySet):
    def today(self, today=None):
        if today is None:
            today = timezone.localdate()
        return self.filter(date=today)

    def upcoming(self, today=None):
        if today is None:
            today = timezone.localdate()
        return self.filter(date__gt=today)


class Event(models.Model):
    objects = EventQuerySet.as_manager()

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="events",
    )
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)

    class Meta:
        verbose_name = "evento"
        verbose_name_plural = "eventos"

    def __str__(self):
        return self.title
