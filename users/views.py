from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from catalog.models import Favourite, Saved
from users.forms import SignUpForm


@login_required
def user_profile(request, username):
    # Get the user object based on the username parameter
    user = User.objects.get(username=username)
    favs, created = Favourite.objects.get_or_create(user=user)
    saved, created = Saved.objects.get_or_create(user=request.user)
    if not request.user.is_superuser:
        return render(request, 'user_page.html', {'user': user, 'favourites': favs, 'saved': saved})
    return redirect(request.GET.get('next', 'index'))


# login_user function
def LoginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user != None and not user.is_superuser:
            login(request, user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return render(request, 'main/main.html', {'message': messages.error(request, 'Enter your data correctly')})

# logout function

@login_required
def LogoutUser(request):
    logout(request)
    request.user = None
    return HttpResponseRedirect('')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST, user = request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect(request.GET.get('next', 'index'))
        else:
            return redirect('/change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'change_password.html', {'form': form})

def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            except Exception as e:
                form.add_error(None, "Неправильно введені дані")
        else:
            messages.error(request, 'Enter your data correctly')
    return render(request, 'main/main.html', {'form': form})


def favourites(request, movie):
    return HttpResponseRedirect(reverse('user_profile', args=[movie]))
