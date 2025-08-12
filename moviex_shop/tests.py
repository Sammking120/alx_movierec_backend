from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse

class MovieEndpointsTest(APITestCase):
    def test_trending_movies_success(self):
        response = self.client.get(reverse('trending-movies'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    def test_recommended_movies(self):
        movie_id = 550  # Example: Fight Club
        response = self.client.get(f"/api/movies/recommended/{movie_id}/")
        self.assertEqual(response.status_code, 200)

class FavoriteMovieTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.client = APIClient()
        self.token = self.client.post('/api/movies/auth/login/', {
            'username': 'test', 'password': 'pass'
        }).data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_add_favorite(self):
        response = self.client.post('/api/movies/favorites/add/', {
            'movie_id': 100, 'title': 'Test Movie'
        })
        self.assertEqual(response.status_code, 201)
