from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from catalog.forms import ReviewForm
from catalog.models import Movie, Genre, Review, Favourite, Saved


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
    review = Review.objects.filter(movie=movie).order_by('-created_at')
    form = ReviewForm()
    try:
        favs, created = Favourite.objects.get_or_create(user=request.user)
        saved, created = Saved.objects.get_or_create(user=request.user)
        favs = True if movie in favs.movies.all() else False
        saved = True if movie in saved.movies.all() else False
    except:
        favs, saved = False, False
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            try:
                new_review = Review(user=request.user, movie=movie)
                form = ReviewForm(request.POST, instance=new_review)
                form.save()
                form = ReviewForm()
                redirect('movie', id=id)
            except:
                form.add_error(None, 'Error')
    return render(request, 'catalog/movie_page.html', {'movie': movie, 'form': form, 'reviews': review, 'favs': favs, 'saved': saved})


@login_required
def delete_review(request, movie_id, review_id):
    review = Review.objects.filter(id=review_id)
    review.delete()
    return redirect('movie', id=movie_id)


@login_required
def add_to_fav(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    favourites, created = Favourite.objects.get_or_create(user=request.user)
    favourites.movies.add(movie)
    favourites.save()
    return redirect('movie', id=movie_id)


@login_required
def remove_from_fav(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    favourites = Favourite.objects.get(user=request.user)
    favourites.movies.remove(movie)
    return redirect('movie', id=movie_id)


@login_required
def add_to_saved(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    saved, created = Saved.objects.get_or_create(user=request.user)
    saved.movies.add(movie)
    saved.save()
    return redirect('movie', id=movie_id)


@login_required
def remove_from_saved(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    saved = Saved.objects.get(user=request.user)
    saved.movies.remove(movie)
    return redirect('movie', id=movie_id)


def search(request):
    query = request.GET['query']
    genres = Genre.objects.all()
    movies = Movie.objects.filter(title__contains=query)
    return render(request, 'catalog/catalog_movies.html', {'movies': movies, 'genres': genres})

