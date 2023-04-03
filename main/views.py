from django.shortcuts import render

from catalog.models import Movie


def index(request):
    movies = Movie.objects.all()
    return render(request, 'main/main.html', {'movies': movies})
