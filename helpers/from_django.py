import ast
import csv
import sqlite3

import numpy
import pandas

import helpers


def _parse_bytes(field):
    """ Convert string represented in Python byte-string literal syntax into a
    decoded character string. Other field types returned unchanged.
    """
    result = field
    try:
        result = ast.literal_eval(field)
    finally:
        return result.decode() if isinstance(result, bytes) else field

def retrive_from_django(movie_db):

        con = sqlite3.connect(movie_db)
        with con:
            cur = con.cursor()
            query_set = []
            for row in cur.execute("SELECT movieid, title, genres, poster from movie_movie"):
                query_set.append(row)

            return query_set


def create_movies_django_csv(movie_list):

    movies = {}

    for movie in movie_list:

        print(movie)
        movies[movie] = dict()
        movies[movie]['movieId'] = movie[0]
        movies[movie]['title'] = str(movie[1]).encode("utf-8")
        movies[movie]['genres'] = movie[2]

    fieldnames = ['movieId', 'title', 'genres']
    with open('movies_django.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in movies:
            writer.writerow(movies[item])


def create_films_genres_df(movies_django_file, movie_db):

    django_movies = {}

    try:
        with open(movies_django_file, encoding="utf8") as f:
            for row in f.readlines()[1:]:
                count = sum(line.count(",") for line in row)
                columns = row.split(', ')
                genres_string = _parse_bytes(columns[count])
                django_movies[columns[0]] = dict()
                django_movies[columns[0]]['movieId'] = columns[0]
                title_string = _parse_bytes(columns[1])
                title_string = title_string.replace("\n", "")
                title_string = title_string.replace("(", "")
                title_string = title_string.replace(")", "")
                title_string = title_string.replace(",", "")
                django_movies[columns[0]]['title'] = title_string
                genres_string = _parse_bytes(columns[count])
                genres_string = genres_string.replace("\n", "")
                django_movies[columns[0]]['genres'] = genres_string
                # print(context.django_movies[columns[0]])

    except Exception as e:

        print('File : movies_django.csv - not found ', e)
        list_from_db = helpers.from_django.retrive_from_django(movie_db=movie_db)
        for movie in list_from_db:
            django_movies[movie[0]] = dict()
            django_movies[movie[0]]['movieId'] = movie[0]

            django_movies[movie[0]]['title'] = _parse_bytes(movie[1])
            django_movies[movie[0]]['genres'] = movie[2]
            # print(context.django_movies[movie[0]])

    #print(django_movies)

    genres_dict = {}

    for film, value in django_movies.items():
        genres_list = django_movies[film]['genres']
        genres_list = genres_list.split('|')

        for genre in genres_list:
            if genre not in genres_dict:
                genres_dict[genre] = dict()

    csv_fields = ['movieId']
    for key in genres_dict:
        csv_fields.append(str(key))
    #print(genres_dict)

    movie_ids = {}
    for row, value in django_movies.items():
         movie_ids[row] = dict()

    #print(movie_ids)

    output_films = {}

    for film in movie_ids:
        if film in django_movies:
            genres_list = django_movies[film]['genres']
            genres_list = genres_list.split('|')
            #print(genres_list)
            genres_counted_in_film = len(genres_list)
            #print(genres_counted_in_film)
            ratio = float(1 / genres_counted_in_film)
            genres_tmp_dict = genres_dict.copy()
            #print(genres_tmp_dict)
            output_films[film] = dict()
            output_films[film]['movieId'] = film
            for genre in genres_list:
                if genre in genres_tmp_dict:
                    output_films[film][genre] = ratio
                    genres_tmp_dict.pop(genre, None)
            for genre_left in genres_tmp_dict:
                output_films[film][genre_left] = numpy.nan

    with open('django_films_genres.csv', 'w', newline='') as file:

        writer = csv.DictWriter(file, fieldnames=csv_fields)
        writer.writeheader()
        for item in movie_ids:
            writer.writerow(output_films[item])

    #print(output_films)

    columns = []
    for film, value in django_movies.items():
        genres_list = django_movies[film]['genres']
        genres_list = genres_list.split('|')

        for genre in genres_list:
            if genre not in genres_dict:
                columns.append(genre)

    df = pandas.DataFrame.from_dict(output_films)#, orient='index', columns=columns)
    df = df.T
    #df = df.drop('movieId', axis=1)
    #print(df.loc['tt0499549', :])

    return df
    # print(output_films)