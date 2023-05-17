from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from SPARQLWrapper import SPARQLWrapper, JSON
import urllib.parse
import requests

import xml.etree.ElementTree as ET
from catalog.forms import ReviewForm
from catalog.models import Movie, Genre, Review, Favourite, Saved, Actor, Director, Writer


def catalog(request):
    genres = Genre.objects.all()
    movies = Movie.objects.all()
    if request.method == 'POST':
        if request.POST.get('genre') == 'all':
            movies = movies.order_by(request.POST.get('sort'))
        else:
            movies = Movie.objects.filter(genre=request.POST.get('genre')).order_by(request.POST.get('sort'))
    page = request.GET.get('page', 1)

    paginator = Paginator(movies, 36)
    try:
        count_movie = paginator.page(page)
    except PageNotAnInteger:
        count_movie = paginator.page(1)
    except EmptyPage:
        count_movie = paginator.page(paginator.num_pages)
    return render(request, 'catalog/catalog_movies.html', {'movies': count_movie, 'genres': genres})


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
                   'rating': rating })


def actor(request, actor_id):
    actor = Actor.objects.get(id=actor_id)
    movies = Movie.objects.filter(actor=actor)
    abstract = 'No information'
    # encode query for use in URL
    encoded_query = urllib.parse.quote(actor.first_name + ' ' + actor.last_name)
    # set DBpedia lookup API endpoint
    url = f"https://lookup.dbpedia.org/api/search?query={encoded_query}"

    # send GET request to API endpoint
    response = requests.get(url)

    # extract DBpedia URL from response XML
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        results = root.findall(".//Result")
        if len(results) > 0:
            dbpedia_url = results[0].find("URI").text

            # Set up the DBpedia endpoint URL and the SPARQL query
            endpoint_url = "https://dbpedia.org/sparql"
            query = f"""
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>

            SELECT ?abstract WHERE {{
              <{dbpedia_url}> dbo:abstract ?abstract.
              FILTER (lang(?abstract) = 'en')
            }}
            """

            # Send the SPARQL query to DBpedia
            sparql = SPARQLWrapper(endpoint_url)
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()

            # Print the abstract property value
            abstract = results["results"]["bindings"][0]["abstract"]["value"]

    return render(request, 'catalog/actor_page.html', {'actor': actor, 'movies': movies, 'bio': abstract[:1000]})


def director(request, id):
    director = Director.objects.get(id=id)
    movies = Movie.objects.filter(director=director)
    return render(request, 'catalog/actor_page.html', {'actor': director, 'movies': movies})


def writer(request, id):
    writer = Writer.objects.get(id=id)
    movies = Movie.objects.filter(writer=writer)
    return render(request, 'catalog/actor_page.html', {'actor': writer, 'movies': movies})


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


def save(request):
    for actor in Actor.objects.all():
        actor_uri = '/'
        encoded_query = urllib.parse.quote(f"{actor.first_name} {actor.last_name}")
        # set DBpedia lookup API endpoint
        url = f"https://lookup.dbpedia.org/api/search?query={encoded_query}"

        # send GET request to API endpoint
        response = requests.get(url)

        # extract DBpedia URL from response XML
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            results = root.findall(".//Result")
            if len(results) > 0:
                actor_uri = results[0].find("URI").text

        # Set up the SPARQL endpoint
        sparql = SPARQLWrapper('http://dbpedia.org/sparql')
        sparql.setReturnFormat(JSON)

        # Construct the SPARQL query to retrieve the image property of the resource
        query = f'''
                      SELECT ?image
                      WHERE {{
                          <{actor_uri}> dbo:thumbnail ?image .
                      }}
                  '''

        # Execute the query and extract the image URL
        sparql.setQuery(query)
        results = sparql.query().convert()
        bindings = results['results']['bindings']
        if bindings:
            image_url = bindings[0]['image']['value']
            image_filename, headers = urllib.request.urlretrieve(image_url)
            with open(image_filename, 'rb') as f:
                image_file = File(f)
                actor.image.save(f'{actor.first_name}_{actor.last_name}.jpg', image_file, save=True)
        else:
            print(f"No image found for {actor.first_name} {actor.last_name}")
    return HttpResponse("success")



