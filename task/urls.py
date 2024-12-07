from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.CustomLoginView.as_view(), name='login_view'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('tasks/pending/', views.PendingTasksView.as_view(), name='pending_tasks'),
    path('tasks/completed/', views.CompletedTasksView.as_view(), name='completed_tasks'),

    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:pk>/edit/', views.TaskEditView.as_view(), name='edit_task'),
    path('task/<int:pk>/complete/', views.TaskCompleteAPIView.as_view(), name='task_completed'),
    path('task/<int:pk>/delete/', views.TaskDeleteAPIView.as_view(), name='task_delete'),
]
