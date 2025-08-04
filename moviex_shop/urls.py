from django.urls import path
from .import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register, list_favorites, add_favorite, remove_favorite

urlpatterns = [
    path('trending/', views.trending_movies),
    path('register/', register, name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('favorites/', list_favorites),
    path('favorites/add/', add_favorite),
    path('favorites/delete/<int:movie_id>/', remove_favorite),
]

