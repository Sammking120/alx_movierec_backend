from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tmdb import get_trending_movies

@api_view(['GET'])
def trending_movies(request):
    movies = get_trending_movies()
    return Response(movies)
