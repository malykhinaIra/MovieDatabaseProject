from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Movie, Genre


def catalog(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all()
    return render(request, 'catalog/catalog_movies.html', {'movies': movies, 'genres': genres})


def movie(request, id):
    movie = Movie.objects.get(id=id)
    return render(request, 'catalog/movie_page.html', {'movie': movie})


def search(request):
    query = request.GET['query']
    genres = Genre.objects.all()
    movies = Movie.objects.filter(title__contains=query)
    return render(request, 'catalog/catalog_movies.html', {'movies': movies, 'genres': genres})

