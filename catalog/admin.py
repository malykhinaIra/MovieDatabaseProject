from django.contrib import admin

# Register your models here.
from catalog.models import Movie, Genre, Director, Writer, Actor, Review

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Director)
admin.site.register(Writer)
admin.site.register(Actor)
