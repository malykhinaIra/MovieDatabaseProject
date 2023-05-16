import os
import urllib.request
import sqlite3

from SPARQLWrapper import SPARQLWrapper, JSON


def get_image_url(name):
    # Створити SPARQL-з'єднання з DBpedia
    sparql = SPARQLWrapper('http://dbpedia.org/sparql')
    sparql.setReturnFormat(JSON)

    # Створити URI-ресурсу для актора з бази даних DBpedia
    actor_uri = f'http://dbpedia.org/resource/{name.replace(" ", "_")}'

    # Сконструювати SPARQL-запит для отримання властивості thumbnail для актора
    query = f'''
        SELECT ?image
        WHERE {{
            <{actor_uri}> dbo:thumbnail ?image .
        }}
    '''

    # Виконати запит і отримати результати
    sparql.setQuery(query)
    results = sparql.query().convert()
    bindings = results['results']['bindings']

    if bindings:
        # Повернути URL-адресу зображення
        image_url = bindings[0]['image']['value']
        return image_url
    else:
        return None


def actor():
    # Підключитися до бази даних SQLite
    conn = sqlite3.connect('db22.sqlite3')
    cursor = conn.cursor()

    # Отримати всіх акторів з бази даних
    cursor.execute('SELECT * FROM catalog_actor')
    actors = cursor.fetchall()

    for actor in actors:
        actor_id, first_name, last_name, image = actor

        # Отримати URL-адресу фото актора
        image_url = get_image_url(f'{first_name} {last_name}')

        if image_url:
            # Створити шлях для збереження фото
            image_path = f'catalog/static/catalog/img/{first_name} {last_name}.jpg'

            # Завантажити фото і зберегти його на диск
            urllib.request.urlretrieve(image_url, image_path)

            # Оновити поле image актора в базі даних
            cursor.execute('UPDATE catalog_actor SET image = ? WHERE id = ?',
                           (f'catalog/img/{first_name} {last_name}.jpg', actor_id))

    # Зберегти зміни у базі даних
    conn.commit()

    # Закрити з'єднання з базою даних
    conn.close()


def movie():
    # Підключитися до бази даних SQLite
    conn = sqlite3.connect('db22.sqlite3')
    cursor = conn.cursor()

    # Отримати всіх акторів з бази даних
    cursor.execute('SELECT * FROM catalog_movie')
    movies = cursor.fetchall()

    for movie in movies:
        movie_id, title, description, rating, release_date, runtime, cover_image, created_at, updated_at = movie

        # Отримати URL-адресу фото актора
        image_url = get_image_url(f'{title}')

        if image_url:
            # Створити шлях для збереження фото
            image_path = f'catalog/static/catalog/img/{title}.jpg'

            # Завантажити фото і зберегти його на диск
            urllib.request.urlretrieve(image_url, image_path)

            # Оновити поле image актора в базі даних
            cursor.execute('UPDATE catalog_movie SET cover_image = ? WHERE id = ?',
                           (f'catalog/img/{title}.jpg', movie_id))

    # Зберегти зміни у базі даних
    conn.commit()

    # Закрити з'єднання з базою даних
    conn.close()

actor()