import requests
from decouple import config

TMDB_API_KEY = config('TMDB_API_KEY')
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def get_trending_movies():
    url = f"{TMDB_BASE_URL}/trending/movie/week"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

def get_recommended_movies(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/recommendations"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []
