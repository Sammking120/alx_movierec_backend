
from django.core.management.base import BaseCommand
from moviex_shop.tmdb import get_trending_movies

class Command(BaseCommand):
    help = "Warm TMDb cache"

    def handle(self, *args, **kwargs):
        get_trending_movies()
        self.stdout.write("Warmed trending cache")
