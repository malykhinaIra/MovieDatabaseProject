from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    profile_image = models.ImageField(upload_to='people/profiles/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Director(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.person.__str__()


class Writer(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.person.__str__()


class Actor(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.person.__str__()


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s review for {self.movie.title}"


class Movie(models.Model):
    title = models.CharField(max_length=255)
    director = models.ManyToManyField(Director)
    writer = models.ManyToManyField(Writer)
    actor = models.ManyToManyField(Actor)
    description = models.TextField()
    genre = models.ManyToManyField(Genre)
    rating = models.FloatField()
    release_date = models.DateField()
    runtime = models.PositiveIntegerField()
    cover_image = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Role(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Credit(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='credits')
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.person.full_name} as {self.role.name} in {self.movie.title}"
