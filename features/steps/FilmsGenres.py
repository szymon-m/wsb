import numpy
from behave import *
from hamcrest import assert_that, equal_to, has_entries

import helpers
from helpers.genres import create_data_frame, create_genres_dict, populated_genres_dataframe
from helpers.data_csv import retrive_imdbid, merge_ids

use_step_matcher("re")


@given("Majac plik movies\.csv")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    # context.movies_file = 'movie/csv_data/movies.csv'  # 20 gatunków
    context.movies_file = 'imdb_movies.csv'  # 24 gatunki


@when("kiedy uruchamiam funkcję helpers\.genres\.create_data_frame\(movies_file\)")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.genres_dataframe = create_data_frame(context.movies_file)


@then("otrzymuję pusty pandas Datframe zawierajacy w naglowku wszystkie gatunki filmow")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    expected = 20
    if str(context.movies_file).__contains__('imdb'):
        expected = 24

    assert_that(context.genres_dataframe.columns.size, equal_to(expected))


@given("Posiadajac plik movies csv z filmami i gatunkami")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    #context.movies_file = 'movie/csv_data/movies.csv'  # 20 gatunków
    context.movies_file = 'imdb_movies.csv' # 24 gatunki


@when("kiedy uruchamiam funkcję helpers\.genres\.create_genres_dict\(movies_file\)")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.genres_dict = create_genres_dict(context.movies_file)


@then("funkcja zwraca słownik gatunków")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    expected = 20
    if str(context.movies_file).__contains__('imdb'):
        expected = 24
    assert_that(len(context.genres_dict.keys()), equal_to(expected))


@given("Posiadajac plik movies csv")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # context.movies_file = 'movie/csv_data/movies.csv'  # 20 gatunków
    context.movies_file = 'imdb_movies.csv'  # 24 gatunki

@step("listę id filmow wystepujacycj juz w bazie django")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.data_file = 'data.csv'
    context.links_file = 'movie/csv_data/links.csv'




@when("kiedy wywoluje funkcje helpers\.genres\.populate_dataframe\(movies_file, django_movies_ids\)")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.data_frame = populated_genres_dataframe(context.movies_file, context.links_file, context.data_file)



@then("otrzymuje wypelniona tabele filmow z 0 lub 1 w zaleznosci czy film nalezy do gatunku")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    expected = 4233
    assert_that(context.data_frame.index.size, equal_to(expected))

@given("Mając pliki movies, links i data")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # context.movies_file = 'movie/csv_data/movies.csv'  # 20 gatunków
    context.movies_file = 'imdb_movies.csv'  # 24 gatunki

    context.links_file = 'movie/csv_data/links.csv'
    context.data_file = 'data.csv'
    context.film_genres_file = 'films_genres.csv'


@when(
    "Kiedy zapisuje wazona tabele do pliku csv - helpers\.weighted_genres_to_csv\(movies_file, links_file, data_file\)")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.df_csv = helpers.genres.weighted_genres_to_csv(context.movies_file, context.links_file, context.data_file)



@then("Pojawia się plik films_genres\.csv")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    expected = "72998,1,1,1,1,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan"
    actual = ""

    with open(context.films_genres_file, encoding="utf-8") as f:
        for row in f.readlines()[1:]:
            actual = row
            print(actual)

    assert_that(len(actual), equal_to(len(expected)))


@given("Majac pliki movies\.csv, links\.csv, i data\.csv")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # context.movies_file = 'movie/csv_data/movies.csv'  # 20 gatunków
    context.movies_file = 'imdb_movies.csv'  # 24 gatunki

    context.links_file = 'movie/csv_data/links.csv'
    context.data_file = 'data.csv'


@when("kiedy wywoluje funkcje helpers\.genres\.weighted_film_genres\(movies_file, links_file, data_file\)")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    context.weighted_film_genres = helpers.genres.weighted_film_genres(context.movies_file, context.links_file, context.data_file)


@then("Otrzymuje dataframe z wagami")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # Cutthroat Island (1995)  Action, Adventure, Comedy
    # https: // www.imdb.com / title / tt0112760 /
    expected_film_id_15 = {'Action': 0.3333333333333333, 'Adventure': 0.3333333333333333,
                           'Animation': numpy.nan, 'Children': numpy.nan, 'Comedy': numpy.nan, 'Crime': numpy.nan,
                           'Documentary': numpy.nan, 'Drama': numpy.nan, 'Fantasy': numpy.nan, 'Film-Noir': numpy.nan,
                           'Horror': numpy.nan, 'IMAX': numpy.nan, 'Musical': numpy.nan, 'Mystery': numpy.nan,
                           'Romance': 0.3333333333333333, 'Sci-Fi': numpy.nan, 'Thriller': numpy.nan,
                           'War': numpy.nan, 'Western': numpy.nan, 'no genres listed': numpy.nan, 'Count': 1.0}

    # Toy Story
    expected_film_id_1 = {'Action': numpy.nan, 'Adventure': 0.2, 'Fantasy': 0.2, 'Sci-Fi': numpy.nan, 'Thriller': numpy.nan,
                          'Animation': 0.2, 'Comedy': 0.2, 'Family': 0.2, 'Musical': numpy.nan, 'Romance': numpy.nan, 'Mystery': numpy.nan, 'Western': numpy.nan, 'Drama': numpy.nan, 'History': numpy.nan,
                          'Sport': numpy.nan, 'Horror': numpy.nan, 'Crime': numpy.nan, 'War': numpy.nan, 'Biography': numpy.nan, 'Music': numpy.nan, 'Documentary': numpy.nan,
                          'News': numpy.nan, 'Film-Noir': numpy.nan, 'Short': numpy.nan, 'Count': 1.0}



    actual = context.weighted_film_genres.loc[1].to_dict()
    #assert_that(actual, _is(expected_film_id_1))
    assert_that(actual, has_entries(({'Adventure': 0.2, 'Fantasy': 0.2 , 'Animation': 0.2, 'Comedy': 0.2 , 'Family': 0.2})))


@given("Mam listę identyfikatorow IMDB wystepujacych w bazie")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.data_file = 'data.csv'
    context.imdbid_tt_list = retrive_imdbid(context.data_file)
    context.links_file = 'movie/csv_data/links.csv'


@when("Kiedy pobieram dane ze strony IMDB w oparciu o IMDB ID - helpers\.genres\.create_imdb_movies_csv\(ids_file\)")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    helpers.genres.create_imdb_movies_csv(context.imdbid_tt_list, context.links_file)



@then("Otrzymuje plik imdb_movies\.csv")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    expected_film_genres = {}

    with open('imdb_movies.csv', encoding="utf8") as f:
        for row in f.readlines()[1:]:
            columns = row.split(',')
            expected_film_genres[columns[0]] = dict()
            expected_film_genres[columns[0]]['movieId'] = int(columns[0])
            expected_film_genres[columns[0]]['title'] = columns[1]
            expected_film_genres[columns[0]]['genres'] = columns[2]
            print(expected_film_genres[columns[0]])


    assert_that(expected_film_genres['72998']['movieId'], equal_to(int(72998)))


