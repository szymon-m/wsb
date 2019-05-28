from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from movie.models import *
from django.http import HttpResponse
import json
import math
import operator
import random
import csv
from movie.initializer import search_cache, search_index

@csrf_protect
def detail(request, model, id):# opis i detale filmu
    items = []
    try:
        if model.get_name() == 'movie' and id != 'None':
            try:
                d = Popularity.objects.get(movieid_id=id)
                weight = d.weight
                d.delete()
                new_record = Popularity(movieid_id=id, weight=weight + 1)
                new_record.save()
            except:
                new_record = Popularity(movieid_id=id, weight=1)
                new_record.save()
            label = 'actor'
            object = model.objects.get(movieid=id)
    except:
        return render(request, '404.html')
    return render(request, 'movie_details.html'.format(label), {'items': items, 'number': len(items), 'object': object})

def whole_list(request, model, page):# lista filmów
    if page is None:
        return render(request, '404.html')
    page = int(page)
    objects = model.objects.all()
    total_page = int(math.ceil(len(objects) / 10))
    if page > total_page:
        return render(request, '404.html')
    last_item_index = 10 * page if page != total_page else len(objects)
    pages = []
    end_distance = total_page - page
    start_page_num = page - 5 if end_distance >= 5 else page - 10 + end_distance
    end_page_num = page + 5 if page > 5 else 10
    for i in range(start_page_num, end_page_num + 1):
        if 1 <= i <= total_page:
            pages.append(i)
    data = {'items': objects[10 * (page - 1):last_item_index], 'current_page': page, 'page_number': total_page,
            'pages': pages}
    return render(request, '{}_list.html'.format(model.get_name()), data)


def search(request, item, query_string, page):# szukanie filmu
    if item is None or query_string is None or page is None:
        return render(request, '404.html')
    query_string = query_string.replace("%20", " ")
    if item == 'movie':
        result = [search_index.data_in_memory['movie_dict'][movie_id] for movie_id in
                  search_index.search_movie(query_string)]

    else:
        return render(request, '404.html')
    page = int(page)
    total_page = int(math.ceil(len(result) / 10))
    if page > total_page and total_page != 0:
        return render(request, '404.html')
    last_item_index = 10 * page if page != total_page else len(result)
    pages = []
    end_distance = total_page - page
    start_page_num = page - 5 if end_distance >= 5 else page - 10 + end_distance
    end_page_num = page + 5 if page > 5 else 10
    for i in range(start_page_num, end_page_num + 1):
        if 1 <= i <= total_page:
            pages.append(i)
    return render(request, item + '_search.html',
                  {'items': result[10 * (page - 1):last_item_index], 'length': len(result),
                   'query_string': query_string, 'current_page': page, 'page_number': total_page, 'pages': pages})
@csrf_protect
def films_reco(request, id, model):
    data = {}
    movie_dict = search_index.data_in_memory['movie_dict']
    popular_movies = Popularity.objects.all().order_by('-weight')
    popular = []
    for movie in popular_movies[:10]:
        try:
            popular.append({'movieid': movie.movieid_id, 'poster': movie_dict[movie.movieid_id].poster})
        except:
            continue
    data['popular'] = popular
    popular_movie_list = [movie_dict[movie.movieid_id] for movie in popular_movies[:5]]
    data['recommendation'] = get_recommendation(request)#,popular_movie_list


    return render(request, 'films_details.html', data)


def get_recommendation(request):#, popular_movie_list
    result = []
    movie_dict = search_index.data_in_memory['movie_dict']
    added_movie_list = []
    if request.user.is_authenticated:

        genre_stats = {}
        for movie in watched_movies:
            for genre in movie.genres.split('|'):
                genre_stats[genre] = genre_stats.get(genre, 0) + 1
        movie_score = {}
        for movie in unwatched_movies:
            movie_score[movie.movieid] = movie.rate
            for genre in movie.genres.split('|'):
                movie_score[movie.movieid] += genre_stats.get(genre, 0) / len(watched_movies)
        sorted_list = sorted(movie_score.items(), key=operator.itemgetter(1), reverse=True)
        for item in sorted_list:
            movie = movie_dict[item[0]]
            result.append({'movieid': movie.movieid, 'poster': movie.poster})
            added_movie_list.append(movie)
            if len(result) == 8:
                break
    sorted_list = sorted(search_index.data_in_memory['movie_rating'].items(), key=operator.itemgetter(1), reverse=True)
    for item in sorted_list:
        movie = movie_dict[item[0]]
        if  movie not in added_movie_list:#movie not in popular_movie_list and
            result.append({'movieid': movie.movieid, 'poster': movie.poster})
        if len(result) == 10:
            break
    return [result[i] for i in random.sample(range(len(result)), 10)]



