from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # Adicionei AuthenticationForm aqui
from .models import Task
from .forms import TaskForm
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.views.generic import FormView
from rest_framework import generics, permissions
from .serializers import TaskSerializer, UserSerializer


def home(request):
    return render(request, 'home.html')

class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'usuarios/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # Apenas salva o usuário, sem autenticar
        messages.success(self.request, "Conta criada com sucesso! Agora faça login para acessar o sistema.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request, error if field == '__all__' else f"{field.capitalize()}: {error}"
                )
        return self.render_to_response(self.get_context_data(form=form))

class CustomLoginView(FormView):
    template_name = 'usuarios/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)  # Aqui chamamos o login corretamente

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = redirect(self.get_success_url())
            response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Strict')
            response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, samesite='Strict')

            messages.success(self.request, "Login realizado com sucesso!")
            return response
        else:
            messages.error(self.request, "Credenciais inválidas.")
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('tasks')  # Garante que o redirecionamento funciona


class CustomLogoutView(LogoutView):
    next_page = '/'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        messages.success(request, "Logout realizado com sucesso!")
        return response

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tarefas/tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, datecompleted__isnull=True).order_by('-created')

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = self.request.user
            task.created = timezone.now()
            task.updated = timezone.now()
            task.save()
            messages.success(request, "Tarefa criada com sucesso!")
        return redirect('tasks')

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tarefas/criando_tarefa.html'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.created = timezone.now()
        task.updated = timezone.now()
        task.save()
        messages.success(self.request, "Tarefa criada com sucesso!")
        return redirect('tasks')

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tarefas/criando_tarefa.html'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.updated = timezone.now()
        task.save()
        messages.success(self.request, "Tarefa atualizada com sucesso!")
        return redirect('tasks')

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tarefas/task_detalhe.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = context['task']
        context.update({
            'is_completed': bool(task.datecompleted),
            'is_important': getattr(task, 'important', False)
        })
        return context

class TaskCompleteView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = []
    template_name = 'tarefas/task_detalhe.html'

    def post(self, request, *args, **kwargs):
        task = self.get_object()

        if task.datecompleted is None:
            task.datecompleted = timezone.now()
            task.save()
            messages.success(request, "Tarefa marcada como concluída!")
        else:
            messages.info(request, "Esta tarefa já está concluída.")

        return redirect('completed_tasks')

class CompletedTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tarefas/completed_tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(
            user=self.request.user,
            datecompleted__isnull=False
        ).order_by('-datecompleted')

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tarefas/task_confirm_delete.html'
    success_url = reverse_lazy('completed_tasks')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Tarefa excluída com sucesso!")
        return super().delete(request, *args, **kwargs)

# Views da API
class TaskListAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)