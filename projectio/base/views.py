from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm, TaskForm, TaskEdit
from .models import Project, Employee, Task
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages


def login_page(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


@csrf_protect
def register_page(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    projects = Project.objects.filter(
        Q(client__f_name__icontains=q) |
        Q(client__l_name__icontains=q) |
        Q(name__icontains=q) |
        Q(client__company__icontains=q)
    )

    paginator = Paginator(projects, 6)
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    nums = 'a' * projects.paginator.num_pages

    context = {'projects': projects, 'nums': nums, 'q': q}
    return render(request, 'base/home.html', context)


def project(request, pk):
    project_instance = Project.objects.get(id=pk)
    context = {'project_instance': project_instance}
    return render(request, 'base/project.html', context)


class ProjectsByUserListView(LoginRequiredMixin, generic.ListView):
    model = Project
    template_name = 'base/user_projects.html'

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


@login_required
def employee_info(request, pk):
    employee = Employee.objects.get(id=pk)
    context = {'employee': employee}
    return render(request, 'base/employee.html', context)


def create_project(request):
    form = ProjectForm(initial={'user': request.user})
    if request.method == 'POST':
        form = ProjectForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/create_project.html', context)


def update_project(request, pk):
    project_instance = Project.objects.get(id=pk)
    form = ProjectForm(instance=project_instance)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project_instance)
        if form.is_valid():
            form.save()
            return redirect('project', pk=pk)

    context = {'form': form}
    return render(request, 'base/create_project.html', context)


def update_task(request, pk):
    task_instance = Task.objects.get(id=pk)
    form = TaskEdit(instance=task_instance)
    if request.method == 'POST':
        form = TaskEdit(request.POST, instance=task_instance)
        if form.is_valid():
            form.save()
            return redirect('project', pk=task_instance.project.id)
    context = {'form': form, 'task_instance': task_instance}
    return render(request, 'base/create_task.html', context)


def create_task(request, pk):
    project_instance = Project.objects.get(id=pk)
    form = TaskForm(initial={'project': project_instance})
    if request.method == 'POST':
        form = TaskForm(request.POST, initial={'project': project_instance})
        if form.is_valid():
            form.save()
            return redirect('project', pk=pk)
    context = {'form': form}
    return render(request, 'base/create_task1.html', context)


def delete_project(request, pk):
    project_instance = Project.objects.get(id=pk)
    context = {'project_instance': project_instance}
    if request.method == 'POST':
        project_instance.delete()
        return redirect('home')

    return render(request, 'base/delete_project.html', context)


def delete_task(request, pk):
    task_instance = Task.objects.get(id=pk)
    context = {'task_instance': task_instance}
    if request.method == 'GET':
        task_instance.delete()
        return redirect('project', pk=task_instance.project.id)

    return render(request, 'base/create_task.html', context)
