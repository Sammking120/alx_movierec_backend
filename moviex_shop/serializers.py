from django.contrib.auth.models import User
from rest_framework import serializers
from django.db import models


class RegisterSerializer(serializers.ModelSerializer):
    class Meta: # pyright: ignore[reportIncompatibleVariableOverride]
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user

from .models import FavoriteMovie

class FavoriteMovieSerializer(serializers.ModelSerializer):
    class Meta: # type: ignore
        model = FavoriteMovie
        fields = ['id', 'movie_id', 'title', 'poster_path']