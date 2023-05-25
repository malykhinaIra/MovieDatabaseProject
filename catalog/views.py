import os
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from SPARQLWrapper import SPARQLWrapper, JSON
import urllib.parse
from urllib.request import urlretrieve
import requests

import xml.etree.ElementTree as ET

from requests import HTTPError

from catalog.forms import ReviewForm
from catalog.models import Movie, Genre, Review, Favourite, Saved, Actor, Director

class CatalogView:
    def __init__(self):
        self.genres = Genre.objects.all()
        self.movies = Movie.objects.all()
        self.selected = {}

    def catalog(self, request):
        if request.method == 'POST':
            if request.POST.get('genre') == 'all':
                self.movies = self.movies.order_by(request.POST.get('sort'))
            else:
                self.movies = Movie.objects.filter(genre=request.POST.get('genre')).order_by(request.POST.get('sort'))
                self.selected['genre'] = Genre.objects.get(id=request.POST.get('genre'))
                self.selected['sort'] = request.POST.get('sort')
        page = request.GET.get('page', 1)

        paginator = Paginator(self.movies, 36)
        try:
            count_movie = paginator.page(page)
        except PageNotAnInteger:
            count_movie = paginator.page(1)
        except EmptyPage:
            count_movie = paginator.page(paginator.num_pages)
        return render(request, 'catalog/catalog_movies.html', {'movies': count_movie, 'genres': self.genres, 'selected': self.selected})


    def movie(self, request, id):
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
                    form = ReviewForm
                    redirect('movie', id=id)
                except:
                    form.add_error(None, 'Error')
        average_rating = Review.objects.filter(movie=movie).aggregate(Avg('rating'))['rating__avg']
        if not average_rating:
            rating = range(0)
        else:
            rating = range(int(average_rating))
        return render(request, 'catalog/movie_page.html',
                      {'movie': movie, 'form': form, 'reviews': review, 'favs': favs, 'saved': saved,
                       'rating': rating})


    def actor(self, request, actor_id):
        actor = Actor.objects.get(id=actor_id)
        movies = Movie.objects.filter(actor=actor)
        abstract = self.get_data(actor.biography)
        if not abstract:
            abstract = 'no information'
        return render(request, 'catalog/actor_page.html', {'actor': actor, 'movies': movies, 'bio': abstract[:1000]})


    def director(self, request, id):
        director = Director.objects.get(id=id)
        movies = Movie.objects.filter(director=director)
        abstract = self.get_data(director.biography)
        if not abstract:
            abstract = 'no information'
        return render(request, 'catalog/actor_page.html', {'actor': director, 'movies': movies, 'bio': abstract[:1000]})


    @login_required
    def delete_review(self, request, movie_id, review_id):
        review = Review.objects.filter(id=review_id)
        review.delete()
        return redirect('movie', id=movie_id)


    @login_required
    def add_to_fav(self, request, movie_id):
        movie = Movie.objects.get(id=movie_id)
        favourites, created = Favourite.objects.get_or_create(user=request.user)
        favourites.movies.add(movie)
        favourites.save()
        return redirect('movie', id=movie_id)


    @login_required
    def remove_from_fav(self, request, movie_id):
        movie = Movie.objects.get(id=movie_id)
        favourites = Favourite.objects.get(user=request.user)
        favourites.movies.remove(movie)
        return redirect('movie', id=movie_id)


    @login_required
    def add_to_saved(self, request, movie_id):
        movie = Movie.objects.get(id=movie_id)
        saved, created = Saved.objects.get_or_create(user=request.user)
        saved.movies.add(movie)
        saved.save()
        return redirect('movie', id=movie_id)


    @login_required
    def remove_from_saved(self, request, movie_id):
        movie = Movie.objects.get(id=movie_id)
        saved = Saved.objects.get(user=request.user)
        saved.movies.remove(movie)
        return redirect('movie', id=movie_id)


    def search(self, request):
        query = request.GET['query']
        movies = Movie.objects.filter(title__contains=query)
        return render(request, 'catalog/catalog_movies.html', {'movies': movies, 'genres': self.genres})


    def get_data(self, url):
        endpoint_url = "https://dbpedia.org/sparql"
        query = f"""
                   PREFIX dbo: <http://dbpedia.org/ontology/>
                   PREFIX foaf: <http://xmlns.com/foaf/0.1/>

                   SELECT ?abstract WHERE {{
                     <{url}> dbo:abstract ?abstract.
                     FILTER (lang(?abstract) = 'en')
                   }}
                   """
        sparql = SPARQLWrapper(endpoint_url)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        abstract = results["results"]["bindings"][0]["abstract"]["value"]
        return abstract

    def add_uri(self):
        for director in Director.objects.all():
            director_uri = '/'
            encoded_query = urllib.parse.quote(f"{director.first_name} {director.last_name}")
            # set DBpedia lookup API endpoint
            url = f"https://lookup.dbpedia.org/api/search?query={encoded_query}"

            # send GET request to API endpoint
            response = requests.get(url)

            # extract DBpedia URL from response XML
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                results = root.findall(".//Result")
                if len(results) > 0:
                    director_uri = results[0].find("URI").text

            director.biography = director_uri
            director.save()

    def save(self):
        for director in Director.objects.all():
            uri = self.get_data(director.biography)
            # Set up the SPARQL endpoint
            sparql = SPARQLWrapper('http://dbpedia.org/sparql')
            sparql.setReturnFormat(JSON)

            # Construct the SPARQL query to retrieve the image property of the resource
            query = f'''
                   SELECT ?image
                   WHERE {{
                       <{uri}> dbo:thumbnail ?image .
                   }}
               '''

            # Execute the query and extract the image URL
            sparql.setQuery(query)
            results = sparql.query().convert()
            bindings = results['results']['bindings']

            if bindings:
                image_url = bindings[0]['image']['value']
            else:
                image_url = ''

            # Check if the image file already exists for the director
            image_path = os.path.join('img', f'{director.first_name}_{director.last_name}.jpg')
            if os.path.exists(image_path):
                continue
            # Download the image and save it to the Director model
            try:
                image_filename, headers = urlretrieve(image_url, image_path)
                with open(image_filename, 'rb') as f:
                    image_file = File(f)
                    director.image.save(f'{director.first_name}_{director.last_name}.jpg', image_file, save=True)
            except HTTPError as e:
                pass

# Usage:

catalog_view = CatalogView()

def catalog(request):
    return catalog_view.catalog(request)

def movie(request, id):
    return catalog_view.movie(request, id)

def actor(request, actor_id):
    return catalog_view.actor(request, actor_id)

def director(request, id):
    return catalog_view.director(request, id)

@login_required
def delete_review(request, movie_id, review_id):
    return catalog_view.delete_review(request, movie_id, review_id)

@login_required
def add_to_fav(request, movie_id):
    return catalog_view.add_to_fav(request, movie_id)

@login_required
def remove_from_fav(request, movie_id):
    return catalog_view.remove_from_fav(request, movie_id)

@login_required
def add_to_saved(request, movie_id):
    return catalog_view.add_to_saved(request, movie_id)

@login_required
def remove_from_saved(request, movie_id):
    return catalog_view.remove_from_saved(request, movie_id)

def search(request):
    return catalog_view.search(request)


