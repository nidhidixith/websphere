from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .forms import UserRegisterForm, ProfileCompletionForm, UserUpdateForm, ProfileUpdateForm
from .models import UserProfile
from django.contrib.auth import login, authenticate

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            messages.success(request, f'Your account has been created! Complete your profile')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('complete_profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def success(request):
    return render(request,'users/success.html')


def complete_profile(request):
    if request.method == 'POST':
        profile_form = ProfileCompletionForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('success')
    else:
        profile_form = ProfileCompletionForm()
    return render(request, 'users/complete_profile.html', {'profile_form': profile_form})


def profile(request):
    user = request.user
    return render(request, 'users/profile.html', {'user': user})


def update_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request,'users/update_profile.html', context)

