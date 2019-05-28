import csv

def retrive_imdbid(data_file):

    ids = []

    with open('data.csv') as f:
        for row in f.readlines()[1:]:
            columns = row.split(',')
            imdb_id = columns[0].split('/')[4]
            ids.append(imdb_id)

    return ids


def merge_ids(links_file, imdb_id_list):

    links = {}
    result_list = []
    not_found = []

    with open(links_file) as f:
        for row in f.readlines()[1:]:
            columns = row.split(',')
            movieid = columns[0]
            imdbid = 'tt' + str(columns[1])
            links[imdbid] = int(movieid)

    for item in imdb_id_list:
        for key in links:
            if key == item:
                result_list.append(links[key])
                #del links[key]
            else:
                not_found.append(links[key])
                #del links[key]

    return result_list

    #return links


def create_stripped_ratings_csv(ids_present_in_db, rating_file):

    input_file = {}
    output_file = {}

    with open(rating_file) as f:
        for row in f.readlines()[1:]:
            columns = row.split(',')

            #input_file[[columns[0]]['userId']] = int(columns[0])
            #input_file[columns[0]]['movieId'] = int(columns[1])
            #input_file[columns[0]]['rating'] = float(columns[2])
            input_file.update({int(columns[0]): {'userId': int(columns[0]), 'movieId': int(columns[1]), 'rating' : float(columns[2])}})
            #print(input_file[int(columns[0])])

    for item in ids_present_in_db:

        for key in input_file:
            if key == item:

                output_file.update({int(item): {'userId': int(input_file[key]['userId']), 'movieId': int(input_file[key]['movieId']), 'rating' : float(input_file[key]['rating'])}})
                #print(output_file[key])
                #del links[key]
            #else:
                #not_found.append(links[key])
                #del links[key]

        # if int(columns[0]) == item:
        #
        #     output_file[int(item)]['userId'] = int(columns[0])
        #     output_file[int(item)]['movieId'] = int(columns[1])
        #     output_file[int(item)]['rating'] = float(columns[2])
        #
        #     print(output_file[int(item)])

    fieldnames = ['userId', 'movieId', 'rating']
    with open('stripped_rating.csv', 'w', newline='') as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in output_file:
            writer.writerow(output_file[item])