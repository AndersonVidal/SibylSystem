from django.conf import settings
from django.db import models


class EventQuerySet(models.QuerySet):
    pass


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
