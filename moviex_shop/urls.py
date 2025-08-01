from django.urls import path
from . import views

urlpatterns = [
    path('trending/', views.trending_movies),
]
