from django.http import HttpResponse
from django.shortcuts import render

from catalog.forms import ReviewForm
from catalog.models import Movie, Genre, Review


def catalog(request):
    genres = Genre.objects.all()
    movies = Movie.objects.all()
    if request.method == 'POST':
        if request.POST.get('genre') == 'all':
            movies = movies.order_by(request.POST.get('sort'))
        else:
            movies = Movie.objects.filter(genre=request.POST.get('genre')).order_by(request.POST.get('sort'))
    return render(request, 'catalog/catalog_movies.html', {'movies': movies, 'genres': genres})


def movie(request, id):
    movie = Movie.objects.get(id=id)
    review = Review.objects.filter(movie=movie)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            try:
                new_review = Review(user=request.user, movie=movie)
                form = ReviewForm(request.POST, instance=new_review)
                form.save()
            except:
                form.add_error(None, 'Error')
    return render(request, 'catalog/movie_page.html', {'movie': movie, 'form': form, 'reviews': review})


def search(request):
    query = request.GET['query']
    genres = Genre.objects.all()
    movies = Movie.objects.filter(title__contains=query)
    return render(request, 'catalog/catalog_movies.html', {'movies': movies, 'genres': genres})

