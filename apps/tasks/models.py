from django.conf import settings
from django.db import models


class Task(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendente"
        COMPLETED = "COMPLETED", "Concluída"

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
