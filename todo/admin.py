from django.contrib import admin
from .models import Todo, Category, Tag, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'created_at', 'todo_count')
    search_fields = ('name', 'description')
    list_per_page = 25

    def todo_count(self, obj):
        return obj.todos.count()
    todo_count.short_description = 'Number of Todos'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'todo_count')
    search_fields = ('name',)
    list_per_page = 25

    def todo_count(self, obj):
        return obj.todos.count()
    todo_count.short_description = 'Number of Todos'


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'category', 'completed', 'due_date', 'created_at')
    list_filter = ('completed', 'priority', 'category', 'created_at')
    search_fields = ('title', 'description')
    filter_horizontal = ('tags',)
    date_hierarchy = 'created_at'
    list_per_page = 25
    list_editable = ('completed',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'completed')
        }),
        ('Details', {
            'fields': ('priority', 'due_date', 'category', 'tags', 'owner')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme_preference', 'email_notifications', 'created_at')
    list_filter = ('theme_preference', 'email_notifications')
    search_fields = ('user__username', 'bio')
    list_per_page = 25
