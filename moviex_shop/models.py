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