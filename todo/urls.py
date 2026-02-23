from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='todo_index'),
    path('todo/<int:todo_id>/toggle/', views.toggle_todo, name='toggle_todo'),
    path('todo/<int:todo_id>/delete/', views.delete_todo, name='delete_todo'),
    path('categories/', views.manage_categories, name='manage_categories'),
]
