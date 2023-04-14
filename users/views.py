from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout


from users.forms import SignUpForm

@login_required
def user(request, username):
    if request.user.is_authenticated:
      return render(request, 'user_page.html', {'username': username})

# login function
def Login(request,username):
    if request.user.is_authenticated:
        return HttpResponseRedirect('user_page.html')

# login_user function
def LoginUser(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user != None:
            login(request,user)
            return HttpResponseRedirect(f'user/{username}')
        else:
            messages.error(request,'Enter your data correctly')
            return HttpResponseRedirect('index')

# logout function
def LogoutUser(request):
    logout(request)
    request.user = None
    return HttpResponseRedirect('')

def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return HttpResponseRedirect(f'user/{username}')
    return HttpResponseRedirect('index')


def favourites(request, username):
    return HttpResponse(f"<h2>{username}'s favourites</h2>")
