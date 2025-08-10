from django.urls import path
from .import views
from .views import trending_movies, recommended_movies
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register_user, list_favorites, add_favorite, remove_favorite

urlpatterns = [
    path('trending/', views.trending_movies, name='trending-movies'),
    path('register/', views.register, name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('favorites/', list_favorites),
    path('favorites/add/', add_favorite),
    path('register/', register_user),
    path('trending/', trending_movies),
    path('recommended/<int:movie_id>/', recommended_movies),
    path('favorites/delete/<int:movie_id>/', remove_favorite),
]

