from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'describe', 'important', 'status', 'datecompleted']
        widgets = {
            'status': forms.Select(choices=Task.STATUS_CHOICES),
            'datecompleted': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'title': forms.TextInput(attrs={'placeholder': 'Digite o título', 'class': 'form-control'}),
            'describe': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
