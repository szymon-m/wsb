import csv

def retrive_imdbid(data_file):

    ids = []

    with open(data_file, encoding="utf8") as f:
        for row in f.readlines()[1:]:
            columns = row.split(',')
            imdb_id = columns[0].split('/')[4]
            ids.append(imdb_id)

    print("Imdbs found: " + str(len(ids)))
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
            #print(links)

    for item in imdb_id_list:
        for key in links:
            if key == item:
                result_list.append(links[key])
                #print('ID added' + str(links[key]))
                #del links[key]
            #else:
            #    not_found.append(links[key])
                #del links[key]
                #print('ID not found' + str(links[key]))

    # for key in links:
    #     for item in imdb_id_list:
    #         if key == item:
    #             result_list.append(links[key])
    #             print(links[key])
    #             break
    #         else:
    #             not_found.append(links[key])
    #             print(links[key])
    #             continue

    print("Ids found: " + str(len(result_list)))
    print("ids NOT found: " + str(len(not_found)))
    #print(links)
    return result_list


def create_stripped_ratings_csv(merged_ids_list, rating_file):

    input_file = {}
    output_file = {}

    #print(merged_ids_list)

    with open(rating_file) as f:
        for row in f.readlines()[1:]:
            columns = row.split(',')
            input_file.update({int(columns[1]): {'userId': int(columns[0]), 'movieId': int(columns[1]), 'rating' : float(columns[2])}})
            #print(input_file[int(columns[1])])

    #print(input_file[72998])
    #print(input_file)

    for item in merged_ids_list:
        for key in input_file:
            if key == item:
                #print("ok")
                output_file.update({int(item): {'userId': int(input_file[key]['userId']), 'movieId': int(input_file[key]['movieId']), 'rating' : float(input_file[key]['rating'])}})
                #print(output_file[int(item)])

    fieldnames = ['userId', 'movieId', 'rating']
    with open('stripped_rating.csv', 'w', newline='') as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in output_file:
            writer.writerow((output_file[item]))
