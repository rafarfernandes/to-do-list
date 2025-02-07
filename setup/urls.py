from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from task.views import TaskListAPIView, TaskDetailAPIView  # Importe as views da API

# Rotas da API (usando DefaultRouter)
router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('task.urls')),  # URLs do frontend
    path('api/', include([
        path('tasks/', TaskListAPIView.as_view(), name='api_task_list'),  # Listar e criar tarefas
        path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='api_task_detail'),  # Detalhar, atualizar e deletar tarefas
    ])),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),  # Schema do DRF Spectacular
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),  # Documentação interativa
]