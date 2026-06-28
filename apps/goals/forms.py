from django import forms

from apps.goals.models import Goal


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ["title", "progress", "target_date"]
        widgets = {
            "target_date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "title": "Título",
            "progress": "Progresso (%)",
            "target_date": "Data-alvo (opcional)",
        }


class GoalProgressForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ["progress"]
        labels = {
            "progress": "Progresso (%)",
        }
