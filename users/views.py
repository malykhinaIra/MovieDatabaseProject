from django.http import HttpResponse
from django.shortcuts import render


def user(request, username):
    return HttpResponse(f"<h2>User {username}</h2>")


def login(request):
    return HttpResponse(f"<h2>Log in</h2>")


def signup(request):
    return HttpResponse(f"<h2>Sign up</h2>")


def favourites(request, username):
    return HttpResponse(f"<h2>{username}'s favourites</h2>")
