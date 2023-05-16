from decimal import Decimal

from django.db.models import Avg
from django.shortcuts import render
from users.forms import UserCreationForm

from catalog.models import Movie, Review


def index(request):
    movies = Movie.objects.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')[:10]
    for movie in movies:
        if movie.avg_rating:
           movie.avg_rating = Decimal(movie.avg_rating).quantize(Decimal('0.1'))
        else:
            movie.avg_rating = 0
    return render(request, 'main/main.html', {'movies': movies})

