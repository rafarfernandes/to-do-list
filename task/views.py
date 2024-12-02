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
    template_name = 'register.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Conta criada com sucesso! Bem-vindo(a).")
        return redirect(self.success_url)

    def form_invalid(self, form):
        
        for field, errors in form.errors.items():
            for error in errors:
                if field == '__all__':
                    
                    messages.error(self.request, error)
                else:
                    
                    messages.error(self.request, f"{field.capitalize()}: {error}")
        
        return self.render_to_response(self.get_context_data(form=form))



class CustomLoginView(LoginView):
    template_name = 'login_view.html'
    next_page = reverse_lazy('tasks')



class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')



class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(
            user=self.request.user,
            datecompleted__isnull=True
        ).order_by('-created')

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        tasks = self.get_queryset()  

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.created = timezone.now()
            task.updated = timezone.now()
            task.save()
            return render(request, self.template_name, {'tasks': tasks, 'form': form})

        return render(request, self.template_name, {'tasks': tasks, 'form': form})



class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'criando_tarefa.html'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.created = timezone.now()
        task.updated = timezone.now()
        task.save()
        return redirect('tasks')



class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'criando_tarefa.html'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.updated = timezone.now()
        task.save()
        return redirect('tasks')



class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detalhe.html'
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
    template_name = 'task_detalhe.html'

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        if task.datecompleted is None: 
            task.datecompleted = timezone.now()
            task.save()
        return redirect('tasks')



class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('completed_tasks')

    def get_queryset(self):
        
        return Task.objects.filter(user=self.request.user)



class CompletedTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'completed_tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(
            user=self.request.user,
            datecompleted__isnull=False
        ).order_by('-datecompleted')