from django.contrib import admin
from .models import Task, Category, Tag


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'completed', 'category', 'due_date', 'created_at')
    list_filter = ('priority', 'completed', 'category')
    search_fields = ('title', 'description')
    filter_horizontal = ('tags',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
