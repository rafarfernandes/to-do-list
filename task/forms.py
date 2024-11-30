from django import forms 
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'describe', 'important', 'status']
        widgets = {
            'status': forms.Select(choices=[
                ('pendente', 'Pendente'),
                ('completa', 'Completa')
            ])
        }