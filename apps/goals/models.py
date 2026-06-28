from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class GoalQuerySet(models.QuerySet):
    def active(self):
        return self.filter(progress__lt=100)


class Goal(models.Model):
    objects = GoalQuerySet.as_manager()

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="goals",
    )
    title = models.CharField(max_length=255)
    progress = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    target_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "meta"
        verbose_name_plural = "metas"

    def __str__(self):
        return self.title
