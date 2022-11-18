from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Это имя пользователя уже существует!'})
        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Пароли не совпадают'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'Имя пользователя или пароль не существуют! Посторите попытку!'})
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
@login_required
def createtask(request):
    if request.method == 'GET':
        return render(request, 'todo/createtask.html', {'form': TaskForm()})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtask.html', {'form': TaskForm(), 'error': 'Переданы неверные данные! Попробуйте ещё раз!'})

@login_required
def edittask(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'todo/edittask.html', {'task': task, 'form': form})
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/edittask.html', {'task': task, 'form': form, 'error': 'Переданы неверные данные! Попробуйте ещё раз!'})


@login_required
def currenttodos(request):
    tasks = Task.objects.filter(user=request.user, datecomplited__isnull=True)
    return render(request, 'todo/currenttodos.html', {'tasks': tasks})


@login_required
def completedtasks(request):
    tasks = Task.objects.filter(user=request.user, datecomplited__isnull=False).order_by('-datecomplited')
    return render(request, 'todo/completedtasks.html', {'tasks': tasks})


@login_required
def completetask(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == 'POST':
        task.datecomplited = timezone.now()
        task.save()
        return redirect('currenttodos')

@login_required
def deletetask(request, task_pk):
   task = get_object_or_404(Task, pk=task_pk, user=request.user)
   if request.method == 'POST':
        task.delete()
        return redirect('currenttodos')
