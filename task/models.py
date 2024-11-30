from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('completa', 'Completa'),
    ]

    title = models.CharField(max_length=100)
    describe = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)  # Define automaticamente a data de criação
    updated = models.DateTimeField(auto_now=True)  # Atualiza automaticamente ao salvar
    datecompleted = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')  # Campo de status
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - by: {self.user.username}"
