from django.urls import path
from .views import (
    home, 
    RegisterView, 
    CustomLoginView, 
    CustomLogoutView, 
    TaskListView, 
    TaskCreateView, 
    TaskUpdateView, 
    TaskDetailView, 
    TaskCompleteView, 
    TaskDeleteView, 
    CompletedTaskListView,
    TaskListAPIView,  # Nova view da API
    TaskDetailAPIView,  # Nova view da API
)

urlpatterns = [
    path('', home, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('tasks/', TaskListView.as_view(), name='tasks'),
    path('tasks/completed/', CompletedTaskListView.as_view(), name='completed_tasks'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/create/', TaskCreateView.as_view(), name='create_task'),
    path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='edit_task'),
    path('task/<int:pk>/complete/', TaskCompleteView.as_view(), name='task_completed'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # Endpoints da API
    path('api/tasks/', TaskListAPIView.as_view(), name='api_task_list'),
    path('api/tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='api_task_detail'),
]