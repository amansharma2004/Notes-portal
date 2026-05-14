from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm
from .models import StudentProfile
from notes.models import Subject, Note

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request.POST or None)
    msg = ""

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                StudentProfile.objects.get_or_create(user=user)
                return redirect('home')
            else:
                msg = "Invalid username or password."

    return render(request, 'login.html', {'form': form, 'msg': msg})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm(request.POST or None)
    msg = ""

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                msg = "Username already taken."
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                StudentProfile.objects.create(user=user)
                # auto-login then go to main notes page
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                return redirect('home')
        else:
            msg = "Please fix the errors."

    return render(request, 'register.html', {'form': form, 'msg': msg})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')