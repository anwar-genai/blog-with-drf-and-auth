from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .forms import ProfileForm


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'accounts/index.html')


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('accounts:dashboard')
    else:
        form = AuthenticationForm(request)
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, 'accounts/dashboard.html')


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('accounts:login')


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('accounts:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    return render(request, 'accounts/profile.html')


@login_required
def profile_edit(request: HttpRequest) -> HttpResponse:
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_edit.html', {'form': form})
