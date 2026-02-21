from django.shortcuts import render, redirect
from .models import Todo


def index(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Todo.objects.create(title=title)
        return redirect('todo_index')

    todos = Todo.objects.order_by('-created_at')
    return render(request, 'todo/index.html', {'todos': todos})
