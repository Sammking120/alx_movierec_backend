from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .tmdb import get_trending_movies
from .serializers import RegisterSerializer, FavoriteMovieSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import FavoriteMovie

@api_view(['GET'])
def trending_movies(request):
    movies = get_trending_movies()
    return Response(movies)

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=201)
    return Response(serializer.errors, status=400)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favorites(request):
    favorites = FavoriteMovie.objects.filter(user=request.user)
    serializer = FavoriteMovieSerializer(favorites, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request):
    data = request.data.copy()
    data['user'] = request.user.id
    serializer = FavoriteMovieSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favorite(request, movie_id):
    try:
        fav = FavoriteMovie.objects.get(user=request.user, movie_id=movie_id)
        fav.delete()
        return Response({"message": "Removed from favorites"}, status=204)
    except FavoriteMovie.DoesNotExist:
        return Response({"error": "Not found"}, status=404)