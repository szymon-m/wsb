from behave import *
from hamcrest import assert_that, equal_to
import pandas
import helpers
from helpers.data_csv import retrive_imdbid
from helpers.data_frame import create_user_ratings_table

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
    # duża baza item[0] = 'tt0114709'

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

    expected_tt0499549 = 72998 #mała baza ratings.csv
    expected_tt0449088 = 53125 #mała baza ratings.csv

    expected_tt0113189 = 10  #duża baza ratings.csv
    expected_tt0114709 = 1   #duża baza

    expected_20m = 4336 # 3649 wspólnych filmów  duża baza 4336
    expected_100k = 3649
    actual = context.ids_present_in_db

    assert_that(len(actual), equal_to(expected_20m))
    assert_that(actual[0], equal_to(expected_tt0499549)) # mała baza
    assert_that(actual[1], equal_to(expected_tt0449088)) # mała baza
    #assert_that(actual[0], equal_to(expected_tt0114709))
    #assert_that(actual[1], equal_to(expected_tt0113189))

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


@when("kiedy uruchamiam funkcję helpers\.data_csv\.create_stripped_ratings_csv\(merged_ids_list,rating_file\)")
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
                userId = int(columns[0])
                movieId = int(columns[1])
                rating = float(columns[2])
                actual.append((userId , movieId, rating))
                x += 1

    expected_100k = (41569, 72998, 4.0)
    expected_20m = (138479, 72998, 2.0)

    assert_that(actual[0], equal_to(expected_20m))


@given("Z plikow stripped_ratings\.csv")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.stripped_rating_file = 'stripped_rating.csv'


@when("Kiedy wywoluje funkcje helpers\.data_frame\.create_user_ratings_table\(rating_file\)")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.user_ratings_df = helpers.data_frame.create_user_ratings_table(context.stripped_rating_file)


@then("Otrzymuje macierz user_ratings typu pandas\.DataFrame")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert_that(context.user_ratings_df, equal_to(type(pandas.DataFrame)))


