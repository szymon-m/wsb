from django.conf.urls import url
from . import views
from . import models

urlpatterns = [
    url(r'^', views.load, name='load'),
    ]
