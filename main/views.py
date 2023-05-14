from decimal import Decimal

from django.db.models import Avg
from django.shortcuts import render
from users.forms import UserCreationForm

from catalog.models import Movie, Review


def index(request):
    movies = Movie.objects.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')
    for movie in movies:
        movie.avg_rating = Decimal(movie.avg_rating).quantize(Decimal('0.1'))
    return render(request, 'main/main.html', {'movies': movies})

