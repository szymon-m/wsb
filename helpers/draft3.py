import numpy
import pandas
from helpers.data_csv import retrive_imdbid, merge_ids

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
links_file = '../movie/csv_data/links.csv'
data_file = '../data.csv'

imdb_id_list = retrive_imdbid(data_file)
movie_ids = merge_ids(links_file, imdb_id_list)

#==================================
# losowa tabela ratingów
rates = [numpy.nan,1,2,3,4,5]
df_random = pandas.DataFrame(numpy.random.choice(rates, size=(100,4336), p=[0.975,0.005,0.005,0.005,0.005,0.005]), index=range(1,101), columns=movie_ids)
df_random.replace(0, numpy.nan)
df_random.loc[:, 'Count'] = df_random.count(axis=1)
df_random = df_random[df_random.Count > 10]
print(df_random)














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

