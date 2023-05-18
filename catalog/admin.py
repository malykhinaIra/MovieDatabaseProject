from django.contrib import admin

# Register your models here.
from catalog.models import Movie, Genre, Director, Actor, Review, Favourite, Saved

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Director)
admin.site.register(Actor)
admin.site.register(Favourite)
admin.site.register(Saved)
