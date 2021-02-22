from django import forms
from .models import Trainer


class TrainerNew(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['name', 'tagtext', 'summary']
