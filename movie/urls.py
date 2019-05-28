from django.conf.urls import url
from . import views
from . import models

urlpatterns = [
    url(r'^movie_all/(?P<page>\d*)', views.whole_list, {'model': models.Movie}, name='whole_list'),
    url(r'^movie_detail/(?P<id>.*)', views.detail, {'model': models.Movie}, name='movie_detail'),
    url(r'^search/(?P<item>.*)/(?P<query_string>.*)/(?P<page>\d*).*', views.search, name='search'),
    url(r'^films_detail/(?P<id>.*)', views.films_reco,{'model':models.Movie}, name='films_reco'), 
    
]
