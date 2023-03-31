from django.contrib import admin

# Register your models here.
from catalog.models import Movie, Review, Person, Role, Credit, Genre, Director, Writer, Actor

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Person)
admin.site.register(Role)
admin.site.register(Credit)
admin.site.register(Genre)
admin.site.register(Director)
admin.site.register(Writer)
admin.site.register(Actor)
