from django.http import HttpResponse
from django.shortcuts import render


def catalog(request):
    return render(request, 'catalog/catalog_movies.html')


def movie(request, id):
    return render(request, 'catalog/movie_page.html')


def search(request):
    query = request.GET['query']
    return HttpResponse(f"<h2>Search for '{query}'</h2>")

