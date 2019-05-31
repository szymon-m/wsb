from imdbpie import Imdb
from helpers.data_csv import retrive_imdbid, merge_ids

imdb = Imdb()



data_file = '../data.csv'
imdbid_tt_list = retrive_imdbid(data_file)

links = {}

with open("../movie/csv_data/links.csv", encoding="utf8") as f:
    for row in f.readlines()[1:]:
        columns = row.split(',')
        tt_id = 'tt' + columns[1]
        links[tt_id] = int(columns[0])

movies = {}
x = 0

for tt in imdbid_tt_list:
    if x < 5:
        if tt in links:
            movie = imdb.get_title_genres(tt)
            movies[links[tt]] = dict()
            movies[links[tt]]['title'] = movie['title']
            movies[links[tt]]['genres'] = ('|').join(movie['genres'])

            x += 1
            print(movies[links[tt]])

print(movies)

# def single_quote(s):
#     if len(s) == 0:
#         return 'None'
#     if s.find('\'') != -1:
#         return s.replace("\'", "\'\'")
#     else:
#         return s
#title  = single_quote(str(movie['base']['title']))
#genres = str(movie['genres'])

#print(title)
#print(genres)



