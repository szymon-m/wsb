from behave import *
import hamcrest
from hamcrest import assert_that, equal_to

import helpers
from helpers.data_csv import retrive_imdbid

use_step_matcher("re")


@given("Posiadajac plik data\.csv")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.data_file = 'data.csv'


@when("Gdy uruchamiam helpers\.data_csv\.retrive_imdbid\(data_file\)")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.imdbId_list = helpers.data_csv.retrive_imdbid(context.data_file)


@then("Powinienem w pierwszym wierszu otrzymac identyfikator IMDB tt0499549")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    expected = 'tt0499549'
    actual = context.imdbId_list[0]

    assert_that(actual, equal_to(expected))


@given("Majac plik links\.csv z kolumnami movieId oraz imdbId")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.links_file = 'movie/csv_data/links.csv'
    context.data_file = 'data.csv'


@step("I Jednoczesnie kiedy posiadam liste identyfikatorow imdbid z pliku data\.csv")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.imdbId_list = helpers.data_csv.retrive_imdbid(context.data_file)
    assert_that(len(context.imdbId_list), equal_to(5043))


@when("Kiedy uruchamiam funkcję helpers\.data_csv\.merge_ids\(links_file, idmb_id_list\)")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.ids_present_in_db = helpers.data_csv.merge_ids(context.links_file, context.imdbId_list)


@then("Otrzymuje listę id filmow ktore juz sa w bazie")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # imdbid = tt0499549   id = 72998
    # imdbid = tt0449088   id = 53125

    expected_tt0499549 = 72998
    expected_tt0449088 = 53125

    expected = 3649 # 3649 wspólnych filmów
    actual = context.ids_present_in_db

    assert_that(len(actual), equal_to(expected))
    assert_that(actual[1], equal_to(expected_tt0449088))
    assert_that(actual[0], equal_to(expected_tt0499549))

    #assert_that(actual[72998], equal_to('tt0499549'))


@given("Mając listę identyfikatorow filmow wystepujacych w bazie")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.links_file = 'movie/csv_data/links.csv'
    context.data_file = 'data.csv'
    context.imdbId_list = helpers.data_csv.retrive_imdbid(context.data_file)
    assert_that(len(context.imdbId_list), equal_to(5043))
    context.ids_present_in_db = helpers.data_csv.merge_ids(context.links_file, context.imdbId_list)

@step("oraz plik ratings\.csv")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.rating_file = 'movie/csv_data/ratings.csv'


@when("kiedy uruchamiam funkcję helpers\.data_csv\.create_stripped_ratings_csv\(ids_present_in_db,rating_file\)")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    helpers.data_csv.create_stripped_ratings_csv(context.ids_present_in_db, context.rating_file)


@then("otrzymam plik stripped_rating\.csv")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    actual = []
    x = 0
    rating_file = 'stripped_rating.csv'
    with open(rating_file) as f:
        for row in f.readlines()[1:]:
            if x == 1:
                break
            else:
                columns = row.split(',')
                userId = columns[0]
                movieId = columns[1]
                rating = columns[2]
                actual[0] = (userId,movieId,rating)
                x += 1

    expected = (1,1,5.0)

    assert_that(actual[0], equal_to(expected))