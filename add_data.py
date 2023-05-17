import csv, sqlite3
from datetime import datetime
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def main():
    database = "db22.sqlite3"

    # --------- Movie Database ------------
    # movie_data_0325.csv column name:
    # Movie_ID, Year, Rank, Title, Description, Duration, Genre, Rating, Metascore, Votes, Gross_Earning_in_Mil, Director, Actor
    # create a database connection
    conn = create_connection(database)
    cur = conn.cursor()

    # insert movie records
    unique_directors = set()
    with open('movie_data_0325.csv', 'r', encoding='utf8') as fin:
        # csv.DictReader uses first line in file for column headings by default
        to_db = []
        reader = csv.DictReader(fin)
        for row in reader:
            dr_name = row['Director']
            if dr_name in unique_directors:
                continue  # Пропустити режисера, якщо він вже присутній
            unique_directors.add(dr_name)
            columns = dr_name.split(' ')
            column1 = columns[0] if columns else ''  # Перша частина колонки
            column2 = columns[1] if len(columns) > 1 else ''  # Друга частина колонки (якщо є)
            to_db.append((column1, column2, '/', '0'))

    cur.executemany("""INSERT INTO catalog_director
    				(first_name, last_name, image, biography)
    				VALUES (?, ?, ?, ?);""", to_db)
    conn.commit()
    conn.close()


def actor():
    database = "db22.sqlite3"

    # --------- Movie Database ------------
    # movie_data_0325.csv column name:
    # Movie_ID, Year, Rank, Title, Description, Duration, Genre, Rating, Metascore, Votes, Gross_Earning_in_Mil, Director, Actor
    # create a database connection
    conn = create_connection(database)
    cur = conn.cursor()

    # insert movie records
    unique_directors = set()
    with open('movie_data_0325.csv', 'r', encoding='utf8') as fin:
        # csv.DictReader uses first line in file for column headings by default
        to_db = []
        reader = csv.DictReader(fin)
        for row in reader:
            dr_name = row['Actor']
            if dr_name in unique_directors:
                continue  # Пропустити режисера, якщо він вже присутній
            unique_directors.add(dr_name)
            columns = dr_name.split(' ')
            column1 = columns[0] if columns else ''  # Перша частина колонки
            column2 = columns[1] if len(columns) > 1 else ''  # Друга частина колонки (якщо є)
            to_db.append((column1, column2, '/'))

    cur.executemany("""INSERT INTO catalog_actor
        				(first_name, last_name, image)
        				VALUES (?, ?, ?);""", to_db)
    conn.commit()
    conn.close()


def genre():
    database = "db22.sqlite3"

    # --------- Movie Database ------------
    # movie_data_0325.csv column name:
    # Movie_ID, Year, Rank, Title, Description, Duration, Genre, Rating, Metascore, Votes, Gross_Earning_in_Mil, Director, Actor
    # create a database connection
    conn = create_connection(database)
    cur = conn.cursor()
    # insert movie records

    unique_genres = set()
    with open('movie_data_0325.csv', 'r', encoding='utf8') as fin:
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin)
        for col in dr:
            unique_genres.add(col['Genre'])

    to_db = [(genre,) for genre in unique_genres]

    cur.executemany("INSERT INTO catalog_genre (name) VALUES (?)", to_db)

    conn.commit()
    conn.close()


def movie():
    database = "db22.sqlite3"

    # --------- Movie Database ------------
    # movie_data_0325.csv column name:
    # Movie_ID, Year, Rank, Title, Description, Duration, Genre, Rating, Metascore, Votes, Gross_Earning_in_Mil, Director, Actor
    # create a database connection
    conn = create_connection(database)
    cur = conn.cursor()
    # insert movie records

    with open('movie_data_0325.csv', 'r', encoding='utf8') as fin:
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin)  # default delimiter: comma
        to_db = [(col['Title'], col['Description'], col['Rating'], col['Year'], col['Duration'], '/', datetime.now(),
                  datetime.now()) for col in dr]

    cur.executemany("""INSERT INTO catalog_movie 
            				(title, description, rating, release_date, runtime, cover_image, created_at, updated_at) 
            				VALUES (?, ?, ?, ?, ?, ?, ?, ?);""", to_db)

    conn.commit()
    conn.close()


def movie_director():
    database = "db22.sqlite3"

    # --------- Movie Database ------------
    # movie_data_0325.csv column name:
    # Movie_ID, Year, Rank, Title, Description, Duration, Genre, Rating, Metascore, Votes, Gross_Earning_in_Mil, Director, Actor

    # create a database connection
    conn = sqlite3.connect(database)
    cur = conn.cursor()

    # insert movie records
    to_db = []
    with open('movie_data_0325.csv', 'r', encoding='utf8') as fin:
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin)  # default delimiter: comma
        for row in dr:
            dr_name = row['Director']
            columns = dr_name.split(' ')
            column1 = columns[0] if columns else ''  # Перша частина колонки
            column2 = columns[1] if len(columns) > 1 else ''  # Друга частина колонки (якщо є)

            # Запит до бази даних для отримання ID режисера за ім'ям
            cur.execute("SELECT id FROM catalog_director WHERE first_name = ? and last_name = ?", (column1, column2,))
            result = cur.fetchone()
            director_id = result[0] if result else None

            movie_name = row['Title']
            cur.execute("SELECT id FROM catalog_movie WHERE title = ?", (movie_name,))
            result = cur.fetchone()
            movie_id = result[0] if result else None

            if movie_id is not None and director_id is not None:
                to_db.append((movie_id, director_id))

    cur.executemany("INSERT INTO catalog_movie_director (movie_id, director_id) VALUES (?, ?);", to_db)
    conn.commit()
    conn.close()


def movie_actor():
    database = "db22.sqlite3"

    # --------- Movie Database ------------
    # movie_data_0325.csv column name:
    # Movie_ID, Year, Rank, Title, Description, Duration, Genre, Rating, Metascore, Votes, Gross_Earning_in_Mil, Director, Actor

    # create a database connection
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    # insert movie records
    to_db = []
    with open('movie_data_0325.csv', 'r', encoding='utf8') as fin:
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin)  # default delimiter: comma
        for row in dr:
            dr_name = row['Actor']
            columns = dr_name.split(' ')
            column1 = columns[0] if columns else ''  # Перша частина колонки
            column2 = columns[1] if len(columns) > 1 else ''  # Друга частина колонки (якщо є)

            # Запит до бази даних для отримання ID режисера за ім'ям
            cur.execute("SELECT id FROM catalog_actor WHERE first_name = ? and last_name = ?", (column1, column2,))
            result = cur.fetchone()
            director_id = result[0] if result else None

            movie_name = row['Title']
            cur.execute("SELECT id FROM catalog_movie WHERE title = ?", (movie_name,))
            result = cur.fetchone()
            movie_id = result[0] if result else None

            if movie_id is not None and director_id is not None:
                to_db.append((movie_id, director_id))

    cur.executemany("INSERT INTO catalog_movie_actor (movie_id, actor_id) VALUES (?, ?);", to_db)
    conn.commit()
    conn.close()

def movie_genre():
    database = "db22.sqlite3"

    # --------- Movie Database ------------
    # movie_data_0325.csv column name:
    # Movie_ID, Year, Rank, Title, Description, Duration, Genre, Rating, Metascore, Votes, Gross_Earning_in_Mil, Director, Actor

    # create a database connection
    conn = sqlite3.connect(database)
    cur = conn.cursor()

    # insert movie records
    to_db = set()  # Використовуємо множину для зберігання унікальних комбінацій movie_id та genre_id
    with open('movie_data_0325.csv', 'r', encoding='utf8') as fin:
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin)  # default delimiter: comma
        for row in dr:
            genre_name = row['Genre']
            columns = genre_name.split(' ')
            column1 = columns[0] if columns else ''  # Перша частина колонки
            column2 = columns[1] if len(columns) > 1 else ''  # Друга частина колонки (якщо є)

            # Запит до бази даних для отримання ID жанру за назвою
            cur.execute("SELECT id FROM catalog_genre WHERE name = ?", (genre_name,))
            result = cur.fetchone()
            genre_id = result[0] if result else None

            movie_name = row['Title']
            cur.execute("SELECT id FROM catalog_movie WHERE title = ?", (movie_name,))
            result = cur.fetchone()
            movie_id = result[0] if result else None

            if movie_id is not None and genre_id is not None:
                # Додавання комбінації movie_id та genre_id до множини
                to_db.add((movie_id, genre_id))

    cur.executemany("INSERT INTO catalog_movie_genre (movie_id, genre_id) VALUES (?, ?);", to_db)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    movie_genre()
