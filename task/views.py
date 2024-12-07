from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .forms import TaskForm
from django.utils import timezone
from rest_framework import status
from django.contrib.auth.forms import UserCreationForm
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

def home(request):
    return render(request, 'home.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'register.html', {'form': form})


class TaskListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskDetailUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

class PendingTasksView(ListView):
    model = Task
    template_name = 'tasks/pending_tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, datecompleted=None)

class CompletedTasksView(ListView):
    model = Task
    template_name = 'tasks/completed_tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).exclude(datecompleted=None)

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

class TaskEditView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/edit_task.html'
    context_object_name = 'task'

    def get_success_url(self):
        return reverse('task_detail', kwargs={'pk': self.object.pk})

class TaskCompleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)
            if task.datecompleted is None:
                task.datecompleted = timezone.now()
                task.save()
                return Response({"message": "Tarefa marcada como concluída!"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Tarefa já concluída."}, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response({"message": "Tarefa não encontrada."}, status=status.HTTP_404_NOT_FOUND)

class TaskDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)
            task.delete()
            return Response({"message": "Tarefa excluída com sucesso!"}, status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({"message": "Tarefa não encontrada."}, status=status.HTTP_404_NOT_FOUND)
