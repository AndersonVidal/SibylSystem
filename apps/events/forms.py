from django import forms

from apps.events.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "date", "time"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
        }
        labels = {
            "title": "Título",
            "date": "Data",
            "time": "Horário (opcional)",
        }
