from rest_framework import serializers
from task.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'describe', 'status', 'important', 'datecompleted', 'user']
        read_only_fields = ['user']
