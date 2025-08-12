from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .tmdb import get_trending_movies, get_recommended_movies
from .serializers import RegisterSerializer, FavoriteMovieSerializer, MovieSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import FavoriteMovie, Movie
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import OpenApiResponse

class ManualPagination(PageNumberPagination):
    page_size = 10

def paginate_api_list(request, data, serializer_class):
    paginator = ManualPagination()
    page = paginator.paginate_queryset(data, request)
    serializer = serializer_class(page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def trending_movies(request):
    data = get_trending_movies()
    return paginate_api_list(request, data, MovieSerializer)

    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def recommended_movies(request, movie_id):
    data = get_recommended_movies(movie_id)
    serializer = MovieSerializer(data=data, many=True)
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

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

@api_view(['GET', 'POST'])
def create_movie(request):
    if request.method == 'GET':
        # List all movies
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # Validate and create a new movie
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
# ...existing code..

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favorite(request, movie_id):
    try:
        fav = FavoriteMovie.objects.get(user=request.user, movie_id=movie_id)
        fav.delete()
        return Response({"message": "Removed from favorites"}, status=204)
    except FavoriteMovie.DoesNotExist:
        return Response({"error": "Not found"}, status=404)