import ast
import csv

import numpy
import pandas
from imdbpie import Imdb

import helpers.data_csv


def _parse_bytes(field):
    """ Convert string represented in Python byte-string literal syntax into a
    decoded character string. Other field types returned unchanged.
    """
    result = field
    try:
        result = ast.literal_eval(field)
    finally:
        return result.decode() if isinstance(result, bytes) else field

def create_data_frame(movie_file):

    genres = {}
    with open(movie_file, encoding="utf8") as f:
        for row in f.readlines()[1:]:
            count = sum(line.count(",") for line in row)
            columns = row.split(',')
            genres_string = _parse_bytes(columns[count])
            genres_string = genres_string.replace("\n", "")
            genres_string = genres_string.replace("(", "")
            genres_string = genres_string.replace(")", "")
            genres_list = genres_string.split('|')

            for genre in genres_list:
                if genre not in genres:
                    genres[genre] = dict()

    genres_dataframe = pandas.DataFrame({}, columns=genres)
    #print(genres_dataframe.columns.size)
    #print(genres)
    return genres_dataframe


def create_genres_dict(movies_file):

    genres = {}
    with open(movies_file, encoding="utf8") as f:
        for row in f.readlines()[1:]:
            count = sum(line.count(",") for line in row)
            columns = row.split(', ')
            genres_string = _parse_bytes(columns[count])
            genres_string = genres_string.replace("\n", "")
            genres_string = genres_string.replace("(", "")
            genres_string = genres_string.replace(")", "")
            genres_list = genres_string.split('|')

            for genre in genres_list:
                if genre not in genres:
                    genres[genre] = dict()
    #print(genres)
    return genres


def populated_genres_dataframe(movies_file, links_file, data_file):

    imdb_id_list = helpers.data_csv.retrive_imdbid(data_file)
    movie_ids = helpers.data_csv.merge_ids(links_file, imdb_id_list)
    genres_dict = create_genres_dict(movies_file)
    populated_genres_df = pandas.DataFrame({}, columns=genres_dict)

    movies = {}
    with open(movies_file, encoding="utf8") as f:
        for row in f.readlines()[1:]:
            count = sum(line.count(",") for line in row)
            columns = row.split(',')
            genres_string = _parse_bytes(columns[count])
            genres_string = genres_string.replace("\n", "")
            genres_string = genres_string.replace("(", "")
            genres_string = genres_string.replace(")", "")
            genres_list = genres_string.split('|')

            movies[int(columns[0])] = dict()
            movies[int(columns[0])]['genres'] = genres_list
            movies[int(columns[0])]['movieId'] = int(columns[0])

    output_films = {}

    for film in movie_ids:
        if film in movies:
            genres_tmp_dict = genres_dict.copy()
            output_films[film] = dict()
            for genre in movies[film]['genres']:
                if genre in genres_tmp_dict:
                    output_films[film][genre] = int(1)
                    genres_tmp_dict.pop(genre, None)
            for genre_left in genres_tmp_dict:
                output_films[film][genre_left] = numpy.nan

    df_to_append = pandas.DataFrame.from_dict(output_films, orient='index')

    populated_genres_df = populated_genres_df.append(df_to_append)
    #populated_genres_df.loc[:, 'Total'] = populated_genres_df.count(axis=1)
    #print(populated_genres_df.tail())

    return populated_genres_df


def weighted_genres_to_csv(movies_file, links_file, data_file):

    imdb_id_list = helpers.data_csv.retrive_imdbid(data_file)
    movie_ids = helpers.data_csv.merge_ids(links_file, imdb_id_list)
    genres_dict = create_genres_dict(movies_file)

    csv_fields = ['movieId']
    for key in genres_dict:
        csv_fields.append(str(key))

    movies = {}
    with open(movies_file, encoding="utf8") as f:
        for row in f.readlines()[1:]:
            count = sum(line.count(",") for line in row)
            columns = row.split(',')
            genres_string = _parse_bytes(columns[count])
            genres_string = genres_string.replace("\n", "")
            genres_string = genres_string.replace("(", "")
            genres_string = genres_string.replace(")", "")
            genres_list = genres_string.split('|')

            movies[int(columns[0])] = dict()
            movies[int(columns[0])]['genres'] = genres_list
            movies[int(columns[0])]['movieId'] = int(columns[0])

    output_films = {}

    for film in movie_ids:
        if film in movies:
            genres_counted_in_film = len(movies[film]['genres'])
            ratio = float(1 / genres_counted_in_film)
            genres_tmp_dict = genres_dict.copy()
            output_films[film] = dict()
            output_films[film]['movieId'] = int(film)
            for genre in movies[film]['genres']:
                if genre in genres_tmp_dict:
                    output_films[film][genre] = ratio
                    genres_tmp_dict.pop(genre, None)
            for genre_left in genres_tmp_dict:
                output_films[film][genre_left] = numpy.nan


    #TODO: poprawić zapisywanie pliku -> DONE

    with open('films_genres.csv', 'w', newline='') as file:

        writer = csv.DictWriter(file, fieldnames=csv_fields)
        writer.writeheader()
        for item in movies:
            writer.writerow(output_films[item])

    print(output_films)
    return output_films


def weighted_film_genres(movies_file, links_file, data_file):

    df = populated_genres_dataframe(movies_file, links_file, data_file)
    df.loc[:,'Count'] = df.count(axis=1)

    def calculate_weights(row):
        return row / row['Count']

    df[:] = df.apply(calculate_weights, axis=1)
    #print(df)
    #print(df.loc[1].to_dict())
    df.drop(['Count'], axis=1)
    return df


def create_imdb_movies_csv(imdbid_tt_list, links_file):

    links = {}
    with open(links_file, encoding="utf8") as f:
        for row in f.readlines()[1:]:
            columns = row.split(',')
            tt_id = 'tt' + columns[1]
            links[tt_id] = int(columns[0])

    imdb = Imdb()
    movies = {}

    for tt in imdbid_tt_list:

        if tt in links:
            movie = imdb.get_title_genres(tt)
            movies[links[tt]] = dict()
            movies[links[tt]]['movieId'] = int(links[tt])
            movies[links[tt]]['title'] = str(movie['title']).encode('utf-8')
            movies[links[tt]]['genres'] = str(('|').join(movie['genres']).encode('utf-8'))
            print(movies[links[tt]])

    #print(movies)
    #movies_df = pandas.DataFrame.from_dict(movies)
    #print(movies_df)
    #movies_df.to_csv('imdb_movies.csv')

    fieldnames = ['movieId', 'title', 'genres']
    with open('imdb_movies.csv', 'w', newline='') as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in movies:
            writer.writerow(movies[item])


