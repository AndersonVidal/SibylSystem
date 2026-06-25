from django import forms

from apps.tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "due_date"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "title": "Título",
            "due_date": "Prazo (opcional)",
        }
