import numpy
import pandas
from pandas import notna, isna



from helpers.from_django import create_films_genres_df
from helpers.data_csv import retrive_imdbid, merge_ids, create_stripped_ratings_csv
from helpers.genres import weighted_film_genres, create_data_frame
from helpers.data_frame import create_user_ratings_table

#
#stripped_rating_file = '../stripped_rating.csv'
#df = create_user_ratings_table(stripped_rating_file)
# df.loc['Total'] = df.mean(axis=0) # ok
# #df.loc['Total'] = df.sum(axis=1)# pl
# df.loc['RowCount'] = df.count(axis=0) #ok

#columns = df.columns

# cnt = df.loc['RowCount'] #ok
# print(cnt) #ok
# #
# # 888888 *  SUPER OK!!
# #
# df.loc[:,'Count'] = df.count(axis=1)
# df = df[df.Count > 10] # podsumowanie kolumn (ilośc not nan w wierszu > 10
# print(df)
# links_file = '../movie/csv_data/links.csv'
# movies_file = '../imdb_movies.csv'
# data_file = '../data.csv'
# rating_file = '../movie/csv_data/ratings.csv'
#
# imdb_id_list = retrive_imdbid(data_file)
# movie_ids = merge_ids(links_file, imdb_id_list)
# #create_stripped_ratings_csv(movie_ids, rating_file)
#
# stripped_rating_file = '../stripped_rating.csv'
# dfs = create_user_ratings_table(stripped_rating_file)
# print(dfs)
movie_django_file = '../movies_django.csv'
movie_db = "../movie.db"

df = create_films_genres_df(movie_django_file, movie_db)
movie_ids = df.loc[:,'movieId'].to_list()

print(df)

#==================================
# losowa tabela ratingów
rates = [numpy.nan,1,2,3,4,5]
df_random = pandas.DataFrame(numpy.random.choice(rates, size=(100,2926), p=[0.128,0.319,0.006,0.046,0.051,0.450]), index=range(1,101), columns=movie_ids)
df_random = pandas.DataFrame(numpy.random.choice(rates, size=(100,2926), p=[0.900,0.005,0.010,0.010,0.025,0.050]), index=range(1,101), columns=movie_ids)
df_random.replace(0, numpy.nan)
df_random.loc[:, 'Count'] = df_random.count(axis=1)
df_random = df_random[df_random.Count > 10]
print(df_random)



user_list = df_random.index.values
rating_dict = dict()

for user in user_list:
#===
# user profile - czyli
# wziac id filmow ocenionych przez uzykownika (rozne od Nan)

#print(notna(df_random.loc[1]))

    not_na_df_row_1 = notna((df_random.loc[user]))
    is_na_df_row_1 = isna((df_random.loc[user]))
    not_na_df_row_1 = not_na_df_row_1.drop(labels='Count')
    not_na_list = []
    is_na_list = []
    for film_id, value  in not_na_df_row_1.iteritems():
        if value is True:
            not_na_list.append(film_id)

    for film_id, value  in is_na_df_row_1.iteritems():
        if value is True:
            is_na_list.append(film_id)

    print("nie ocenione przez uzytkownika: " + str(len(is_na_list)))
    #print(is_na_list)
    print("ocenione / obejrzane przez uzytkownika: " + str(len(not_na_list)))
    #print(not_na_list)


    # pobrac z dataframe film/genres dany film

    print(numpy.isnan(df.loc['tt0499549','Action']))

    #df = df.drop('movieId', axis=1)
    genres_list = df.columns.values
    print(genres_list[1])

    usr_df = pandas.DataFrame({}, index= ['value','watched_films','avg','delta'], columns=genres_list)
    usr_df = usr_df.astype('float')
    print(usr_df.Action.values.dtype)
    usr_df = usr_df.fillna(0)

    for film in not_na_list:
        for genre in genres_list:
            if pandas.isna(df.loc[film,genre]):
                continue
            else:
                value = df.loc[film, genre]
                #print(value)
                usr_df.loc['value', genre] = value
                usr_df.loc['watched_films', genre] += 1
                #print(df.loc[film,genre])

    #print(usr_df)
    print(usr_df.loc['value'].count())

    genres_count = usr_df.loc['value'].count()
    #usr_df.loc[:,'Non_zero'] = usr_df.astype(bool).count(axis=1)
    usr_df.loc[:,'Total'] = usr_df.sum(axis=1)
    total = usr_df.loc['value', 'Total']
    avg = total / genres_count
    usr_df.loc['avg',:] = avg
    #usr_df.loc['delta',:] = 2
    #usr_df.loc['delta'] = usr_df.loc['value'] - usr_df.loc['avg']
    #print(avg)
    usr_df = usr_df.drop('movieId', axis=1)

    for genre in usr_df.columns.values:
        value = usr_df.loc['value',genre]
        if value == 0:
            continue
        #print(value)
        avg = usr_df.loc['avg',genre]
        #print(avg)
        usr_df.loc['delta',genre] = value - avg
        #print(genre)

    # def calculate_delta(row):
    #     return avg
    #
    #
    #usr_df['delta',:] = usr_df.apply(calculate_delta, axis=1)
    #usr_df = usr_df.drop('Total', axis=1)
    new_columns = usr_df.columns[usr_df.loc[usr_df.last_valid_index()].argsort()]
    usr_df = usr_df[new_columns]
    print(usr_df)

    delta_series = usr_df.loc['delta',:]
    delta_series = delta_series[:10]
    delta_series = delta_series.sort_values(ascending=False)

    if(delta_series[0] < 0) and (delta_series[1] < 0) and (delta_series[2] < 0):
        if(delta_series[0] - delta_series[1]) <0 and (delta_series[0] - delta_series[1]) <= 0.2*(delta_series[0]):

            if(delta_series[1]-delta_series[2]) <0 and (delta_series[1]-delta_series[2]) <= 0.3*(delta_series[1]):
                print(delta_series)

                print(usr_df.loc['value'].to_list())
                print(usr_df.loc['delta'].to_list())
                print(usr_df.loc['avg'].to_list())
                #rating_dict[user] = usr_df.to_dict(0)
                #usr_df.to_csv("founde.csv")


    if(delta_series[0] > 0):
        if (delta_series[0] - delta_series[1]) > 0 and (delta_series[0] - delta_series[1]) >= 0.2 * (delta_series[0]):
            if (delta_series[1] - delta_series[2]) >= 0 and (delta_series[1] - delta_series[2]) >= 0.3 * (delta_series[1]):
                print(delta_series)
                #usr_df.to_csv("founde.csv")
                #rating_dict[user] = usr_df.to_dict(0)
                print(usr_df.loc['value'].to_list())
                print(usr_df.loc['delta'].to_list())
                print(usr_df.loc['avg'].to_list())



print(ratings)

#print(usr_df)

    #if numpy.isnan(df.loc[film])

#df_genres_films = weighted_film_genres(movies_file, links_file, data_file)
#print(df_genres_films)
#df_genres_films = df_genres_films.drop(['Count'], axis=1)

# user = {}
# first_element = not_na_list[0]
#print(df_genres_films.loc[first_element])
#usr_1 = dict()
# df = df.drop('movieId', axis=1)
# col = df.columns.values
#
# usr_df = pandas.DataFrame({}, index= ['value','watched_films','avg','delta'], columns=col)
#
#
# usr_df.loc['value','Action'] = 0.3
# usr_df.loc['value','Action'] += 0.3
# print(usr_df)



#+++++++++++++++++++
#
# for genre_name, value in df_genres_films.loc[first_element].iteritems():
#     if numpy.isnan(value):
#         continue
#     else:
#         if genre_name not in usr_1:
#             usr_1[genre_name] = dict()
#             usr_1[genre_name]['value'] = value
#             usr_1[genre_name]['number_of_watched'] = int(1)
#             usr_1[genre_name]['delta'] = int(0)
#         else:
#             usr_1[genre_name]['value'] += value
#             usr_1[genre_name]['number_of_watched'] += 1
#
#         print(type(usr_1[genre_name]['value']))
#
# sum  = 0
# for genre in usr_1:
#     sum += usr_1[genre]['value']
#
# usr_1['avg'] = sum/len(usr_1)
#
# for genre, inner_dict in usr_1.items():
#    #usr_1[genre]['delta'] = 3
#     inner_dict[2] = 2
#    #for inner, inner_value in inner_dict.items():
#        #print(inner)
#     #   inner[2] = 2
#
#             # if inner == 'delta':
#             #     inner_dict[inner] = 2
#
#     #print(inner_dict['delta'])
#     #inner_dict['delta'] = 1
#     # for inner in inner_dict:
#     #     print(inner)
#
#
#
# # for genre, value in usr_1.items():
# #       for entry_key, entry_value in value:
# #           print(entry_value)
#
#       #usr_1[genre].update([('delta', 1)])
#       #print(genre['delta'])
#       #print(genre['delta'])
#       #genre['delta'] = usr_1['avg']-genre['value']
#
#
# def myprint(d):
#   for k, v in d.items():
#     if isinstance(v, dict):
#       myprint(v)
#     else:
#       print("{0} : {1}".format(k, v))
#
# #myprint(usr_1)
# print(usr_1)

# i dodac do odpowiedniego gatunku wartosci wag do profilu uzytkownika
# i jednoczesnie dodac (jak 1/3 lub 1/2??) ilosc obejrzanych przez uzytkownika filmow z danego gatunku

# profil powinien wygladać nastepująco
# { user_id :
#       { 'Action' : 34.4345,
#         'number_of_watched' : 23 },
#       { 'Drama' : 17.315,
#         'number_of_watched' : 13 },
# } itd.

# dalej liczymy średnią czyli
#           Action      Drama       Comedy      Horror      Sci-Fi
#   value     15          8            4           3           1          średnia   31 /  5  = 6,20 (ilość gatunków)
#   number     3          2            3           7           7
#   avg       6.2        6.2          6.2         6.2         6.2
#   delta    8.80       1.80        -2.20       -3.20       -5.20        delta = value - avg

# sortujemy po malejąco po delta
#          [ 8.80,      1.80,       -2.20 ,     -3.20,      -5.20 ]

# chcemy uzyskać uzytkownika który preferuje pewne gatunki
# wiec delta #1 pozycji > jak 2 x średnia (avg)
# wiec delta #2 pozycji > 50 % delty #1
# wiec delta #3 pozycji > 30 # delty #1













# copy = df_random.loc[:,130578]
# print(copy[2])
# df_random = df_random.drop(130578, axis=1)
# print(df_random)
#=================================
# działająca czesc z wyznaczniem wag w zaleznosci od ilosci gatunkow okreslonych
#==================================
# rectangles = [
#     { 'a' : 1, 'b': 1, 'c': 1},
#     { 'a' : numpy.nan, 'b': numpy.nan, 'c': 1},
#     { 'a' : 1, 'b': numpy.nan, 'c': 1},
# ]
#
# rectangles_df = pandas.DataFrame(rectangles)
# rectangles_df['Count'] = rectangles_df.count(axis=1)
#
# def calculate_area(row):
#    return row / row['Count']
#
#
# rectangles_df[:] = rectangles_df.apply(calculate_area, axis=1)
# print(rectangles_df)
# print("=================================")

