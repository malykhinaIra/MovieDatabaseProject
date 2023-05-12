from django.shortcuts import render
from users.forms import UserCreationForm

from catalog.models import Movie


def index(request):
    movies = Movie.objects.all().order_by('-rating').values()
    return render(request, 'main/main.html', {'movies': movies})

