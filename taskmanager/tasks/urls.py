from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task-list'),
    path('task/<int:pk>/', views.task_detail, name='task-detail'),
    path('task/new/', views.task_create, name='task-create'),
    path('task/<int:pk>/edit/', views.task_update, name='task-update'),
    path('task/<int:pk>/delete/', views.task_delete, name='task-delete'),
    path('categories/', views.category_list, name='category-list'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category-delete'),
]