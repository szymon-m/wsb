import numpy
import pandas


from django.http import HttpResponse
from pandas import notna, isna

from helpers.from_django import create_films_genres_df
from uzytkownik.models import User


# Create your views here.
def load(request):


    movie_django_file = 'movies_django.csv'
    movie_db = "movie.db"

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




        print(numpy.isnan(df.loc['tt0499549','Action']))


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
                    previous_value = usr_df.loc['value',genre]
                    print(previous_value)
                    value = df.loc[film , genre]
                    #brand_new_value = previous_value + new_value

                    usr_df.loc['value', genre] = value
                    usr_df.loc['watched_films', genre] += 1

        print(usr_df.loc['value'].count())

        genres_count = usr_df.loc['value'].count()

        usr_df.loc[:,'Total'] = usr_df.sum(axis=1)
        total = usr_df.loc['value', 'Total']
        avg = total / genres_count
        usr_df.loc['avg',:] = avg

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


        usr_df = usr_df.drop('Total', axis=1)
        new_columns = usr_df.columns[usr_df.loc[usr_df.last_valid_index()].argsort()]
        usr_df = usr_df[new_columns]

        usr_df = usr_df.T
        usr_df = usr_df.sort_values(by='delta', ascending=False)
        usr_df = usr_df.T


        print(usr_df)

        delta_series = usr_df.loc['delta',:]
        delta_series = delta_series[:10]
        delta_series = delta_series.sort_values(ascending=False)

        if(delta_series[0] < 0) and (delta_series[1] < 0) and (delta_series[2] < 0):
            if(delta_series[1] - delta_series[0]) > 0 and (delta_series[1] - delta_series[1]) <= 0.2*(delta_series[0]):

                if(delta_series[1]-delta_series[2]) < 0 and (delta_series[1]-delta_series[2]) <= 0.3*(delta_series[1]):
                    print(delta_series)

                    genres_ordered = ','.join(str(v) for v in usr_df.columns.values)

                    value_str = ','.join(str(v) for v in usr_df.loc['value'].to_list())
                    delta_str = ','.join(str(v) for v in usr_df.loc['delta'].to_list())
                    avg_str = ','.join(str(v) for v in usr_df.loc['avg'].to_list())

                    ratings_str = ','.join(str(v) for v in df_random.loc[user,:].to_list())


                    User.objects.create(value=value_str, delta=delta_str, avg=avg_str, ratings=ratings_str, genres_ordered=genres_ordered)

                    print(usr_df.loc['value'].to_list())
                    print(usr_df.loc['delta'].to_list())
                    print(usr_df.loc['avg'].to_list())
                    #rating_dict[user] = usr_df.to_dict(0)
                    #usr_df.to_csv("founde.csv")


        if(delta_series[0] > 0):
            if (delta_series[0] - delta_series[1]) > 0 and (delta_series[0] - delta_series[1]) >= 0.2 * (delta_series[0]):
                if (delta_series[1] - delta_series[2]) > 0 and (delta_series[1] - delta_series[2]) >= 0.3 * (delta_series[1]):
                    print(delta_series)
                    #usr_df.to_csv("founde.csv")
                    #rating_dict[user] = usr_df.to_dict(0)
                    print(usr_df.loc['value'].to_list())
                    print(usr_df.loc['delta'].to_list())
                    print(usr_df.loc['avg'].to_list())

                    value_str = ','.join(str(v) for v in usr_df.loc['value'].to_list())
                    delta_str = ','.join(str(v) for v in usr_df.loc['delta'].to_list())
                    avg_str = ','.join(str(v) for v in usr_df.loc['avg'].to_list())

                    ratings_str = ','.join(str(v) for v in df_random.loc[user, :].to_list())

                    genres_ordered = ','.join(str(v) for v in usr_df.columns.values)


                    User.objects.create(value=value_str, delta=delta_str, avg=avg_str, ratings=ratings_str, genres_ordered=genres_ordered)

    return HttpResponse("USER RATINGS GENERATOR")