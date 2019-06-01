import sqlite3

from hamcrest import assert_that, equal_to

import helpers
from helpers.from_django import retrive_from_django
from behave import *


use_step_matcher("re")

@given("Mając baze django movie_db")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.movie_db = 'movie.db'


@when("Pobieram dane z bazy - helpers\.from_django\.retrieve_from_django\(movie_db\)")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.query_set = helpers.from_django.retrive_from_django(context.movie_db)


@then("Mam listę filmow")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    actual_first_id = ''

    for row in context.query_set[:1]:
        actual_first_id = row[0]

    expected = 'tt0499549'

    assert_that(actual_first_id, equal_to(expected))


@given("Majac liste filmow")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.movie_db = 'movie.db'
    context.query_set = helpers.from_django.retrive_from_django(context.movie_db)


@when("Kiedy zapisuje je do pliku \.csv - helpers\.from_django\.create_movies_django_csv\(movie_list\)")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    helpers.from_django.create_movies_django_csv(context.query_set)


@then("Otrzymuje plik movies_django\.csv")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    expected_django_movie = {}

    with open('movies_django.csv', encoding="utf8") as f:
        for row in f.readlines()[1:]:
            columns = row.split(',')
            expected_django_movie[columns[0]] = dict()
            expected_django_movie[columns[0]]['movieId'] = columns[0]
            expected_django_movie[columns[0]]['title'] = columns[1]
            expected_django_movie[columns[0]]['genres'] = columns[2]
            print(expected_django_movie[columns[0]])

    assert_that(expected_django_movie['tt0499549']['movieId'], equal_to('tt0499549'))