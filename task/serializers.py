from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Para exibir informações do usuário

    class Meta:
        model = Task
        fields = ['id', 'title', 'describe', 'created', 'updated', 'datecompleted', 'status', 'important', 'user']
        read_only_fields = ['created', 'updated', 'user']  # Campos que não podem ser editados

    def create(self, validated_data):
        # Define o usuário automaticamente como o usuário logado
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Atualiza a tarefa, mas mantém o usuário original
        instance.title = validated_data.get('title', instance.title)
        instance.describe = validated_data.get('describe', instance.describe)
        instance.datecompleted = validated_data.get('datecompleted', instance.datecompleted)
        instance.status = validated_data.get('status', instance.status)
        instance.important = validated_data.get('important', instance.important)
        instance.save()
        return instance