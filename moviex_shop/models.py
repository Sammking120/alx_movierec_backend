from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    title = models.CharField(max_length=255)
    poster_path = models.URLField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'movie_id')
    
# filepath: /home/sammking/Documents/Projects/alx_movierec_backend/moviex_shop/models.py
from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    # Add other fields as needed

    def __str__(self):
        return self.title