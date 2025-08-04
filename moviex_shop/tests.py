from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from rest_framework.test import APIClient

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
