import pandas


def create_user_ratings_table(rating_file):
    ratings_df = pandas.read_csv(rating_file)
    user_ratings_df = ratings_df.pivot(index='userId', columns='movieId', values='rating')
    user_ratings_df = user_ratings_df.fillna(0)
    return user_ratings_df
