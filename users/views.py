from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from applications.models import Application
from users.forms import UserForm


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:index')
    else:
        form = UserForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main:index')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('main:index')

def profile_view(request):
    profile = request.user.profile
    return render(request, 'users/profile.html', {'profile': profile})





@login_required
def my_applications(request):
    """Мои отклики (для соискателя)"""
    if request.user.user_type != 'seeker':
        return redirect('main:index')

    applications = Application.objects.filter(
        applicant=request.user
    ).select_related('vacancy', 'vacancy__company').order_by('-created_at')

    context = {
        'applications': applications,
        'title': 'Мои отклики'
    }
    return render(request, 'users/my_applications.html', context)


@login_required
def favorites(request):
    """Избранные вакансии"""
    if request.user.user_type != 'seeker':
        return redirect('main:index')


    context = {
        'favorites': [],
        'title': 'Избранное'
    }
    return render(request, 'users/favorites.html', context)