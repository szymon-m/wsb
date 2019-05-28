import pandas


def create_user_ratings_table(stripped_rating_file):
    ratings_df = pandas.read_csv(stripped_rating_file)
    user_ratings_df = ratings_df.pivot(index='userId', columns='movieId', values='rating')
    user_ratings_df = user_ratings_df.fillna(0)
    return user_ratings_df
