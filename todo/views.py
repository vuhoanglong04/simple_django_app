from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Todo, Category, Tag


def index(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        priority = request.POST.get('priority', 'medium')
        category_id = request.POST.get('category')
        
        if title:
            todo = Todo.objects.create(
                title=title,
                description=description,
                priority=priority
            )
            if category_id:
                todo.category_id = category_id
                todo.save()
            
            tag_names = request.POST.get('tags', '').split(',')
            for tag_name in tag_names:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    todo.tags.add(tag)
        
        return redirect('todo_index')

    todos = Todo.objects.select_related('category').prefetch_related('tags').order_by('-created_at')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    context = {
        'todos': todos,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'todo/index.html', context)


@require_http_methods(["POST"])
def toggle_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.completed = not todo.completed
    todo.save()
    return JsonResponse({'status': 'success', 'completed': todo.completed})


@require_http_methods(["POST"])
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.delete()
    return JsonResponse({'status': 'success'})


def manage_categories(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        color = request.POST.get('color', '#3498db')
        description = request.POST.get('description', '')
        
        if name:
            Category.objects.create(
                name=name,
                color=color,
                description=description
            )
        return redirect('manage_categories')
    
    categories = Category.objects.prefetch_related('todos').all()
    return render(request, 'todo/categories.html', {'categories': categories})
