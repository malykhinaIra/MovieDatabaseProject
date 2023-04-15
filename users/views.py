from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from users.forms import SignUpForm


@login_required
def user_profile(request, username):
    # Get the user object based on the username parameter
    user = User.objects.get(username=username)
    return render(request, 'user_page.html', {'user': user})


# login_user function
def LoginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user != None and not user.is_superuser:
            login(request, user)
            return HttpResponseRedirect(reverse('user_profile', args=[username]))
        else:
            return render(request, 'main/main.html', {'message':  messages.error(request, 'Enter your data correctly')})


# logout function

@login_required
def LogoutUser(request):
    logout(request)
    request.user = None
    return HttpResponseRedirect('')


def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('user_profile', args=[username]))
        except:
            form.add_error(None, 'Error')
    return render(request, 'main/main.html')


def favourites(request, username):
    return HttpResponse(f"<h2>{username}'s favourites</h2>")
