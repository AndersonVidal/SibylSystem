from datetime import date

from django.conf import settings
from django.db import models


class TaskQuerySet(models.QuerySet):
    def overdue(self, today=None):
        if today is None:
            today = date.today()
        return self.filter(
            status=Task.Status.PENDING,
            due_date__isnull=False,
            due_date__lt=today,
        )

    def pending_not_overdue(self, today=None):
        if today is None:
            today = date.today()
        return self.filter(status=Task.Status.PENDING).filter(
            models.Q(due_date__isnull=True) | models.Q(due_date__gte=today)
        )


class Task(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendente"
        COMPLETED = "COMPLETED", "Concluída"

    objects = TaskQuerySet.as_manager()

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "tarefa"
        verbose_name_plural = "tarefas"

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        return (
            self.status == self.Status.PENDING
            and self.due_date is not None
            and self.due_date < date.today()
        )
