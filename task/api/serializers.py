from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'describe', 'created', 'updated', 'datecompleted', 'status', 'important']
        read_only_fields = ['created', 'updated', 'datecompleted']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.describe = validated_data.get('describe', instance.describe)
        instance.status = validated_data.get('status', instance.status)
        instance.important = validated_data.get('important', instance.important)
        instance.save()
        return instance