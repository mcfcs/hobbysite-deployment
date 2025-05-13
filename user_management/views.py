from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Profile
from .forms import UserRegisterForm, UserEditProfile

def register_view(request):
    """
    @brief Function-Based View for user registration.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def home_view(request):
    current_time = timezone.now()
    return render(request, "homepage.html",  {'current_time': current_time})

@login_required
def profile_view(request):
    """
    @brief Function-Based View for displaying the user's profile.
    """
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'profile.html', {'profile':profile})

@login_required
def profile_update(request):
    """
    @brief Function-Based View for updating display name and email.
    """
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = UserEditProfile(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserEditProfile(instance=profile)

    return render(request, 'profile_update.html', {
        'form': form,
        'profile': profile
    })
