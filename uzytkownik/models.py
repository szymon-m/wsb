from django.db import models

class User(models.Model):

    userid = models.IntegerField(primary_key=True, auto_created=True)
    genres_ordered = models.CharField(max_length=1000)
    value = models.CharField(max_length=1000)
    avg = models.CharField(max_length=1000)
    delta = models.CharField(max_length=1000)
    ratings = models.CharField(max_length=50000)


    def __str__(self):
        return self.movieid + '|' + self.title

    @staticmethod
    def get_name():
        return 'movie'
