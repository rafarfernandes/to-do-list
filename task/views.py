from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from .forms import TaskForm
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'usuarios/register.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Conta criada com sucesso! Bem-vindo(a).")
        return redirect(self.success_url)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request, error if field == '__all__' else f"{field.capitalize()}: {error}"
                )
        return self.render_to_response(self.get_context_data(form=form))


class CustomLoginView(LoginView):
    template_name = 'usuarios/login_view.html'
    next_page = reverse_lazy('tasks')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tarefas/tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        # Exibe apenas as tarefas pendentes
        return Task.objects.filter(
            user=self.request.user,
            datecompleted__isnull=True  # Garantir que a data de conclusão seja nula
        ).order_by('-created')

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.created = timezone.now()
            task.updated = timezone.now()
            task.save()
            messages.success(request, "Tarefa criada com sucesso!")
        tasks = self.get_queryset()  # Para renderizar as tarefas novamente
        return render(request, self.template_name, {'tasks': tasks, 'form': form})


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
        return redirect('tasks')  # Redireciona para a lista de tarefas pendentes


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
            'is_completed': bool(task.datecompleted),  # Verifica se a tarefa foi concluída
            'is_important': getattr(task, 'important', False)  # Se a tarefa for importante
        })
        return context


class TaskCompleteView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = []  # Nenhum campo é necessário para a conclusão
    template_name = 'tarefas/task_detalhe.html'

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        if task.datecompleted is None:
            task.datecompleted = timezone.now()
            task.save()
            messages.success(request, "Tarefa marcada como concluída!")
        return redirect('tasks')  # Redireciona para a lista de tarefas pendentes


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tarefas/task_confirm_delete.html'
    success_url = reverse_lazy('completed_tasks')  # Redireciona para as tarefas concluídas

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Tarefa excluída com sucesso!")
        return super().delete(request, *args, **kwargs)


class CompletedTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tarefas/completed_tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        # Exibe apenas as tarefas concluídas
        return Task.objects.filter(
            user=self.request.user,
            datecompleted__isnull=False  # Garantir que a data de conclusão não seja nula
        ).order_by('-datecompleted')
