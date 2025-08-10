import requests
import logging
from decouple import config
from django.core.cache import cache

# Configure logging
logger = logging.getLogger(__name__)

TMDB_API_KEY = config('TMDB_API_KEY')
TMDB_BASE_URL = "https://api.themoviedb.org/3"

TRENDING_TTL = int(config('TMDB_TRENDING_TTL', default=600))
RECOMM_TTL = int(config('TMDB_RECOMM_TTL', default=1800))


def _fetch_from_tmdb(path, params=None, timeout=6):
    url = f"{TMDB_BASE_URL}{path}"
    params = params or {}
    params['api_key'] = TMDB_API_KEY
    try:
        resp = requests.get(url, params=params, timeout=timeout)
        resp.raise_for_status()
        return resp.json().get('results', [])
    except requests.RequestException as exc:
        logger.exception("TMDb request failed: %s %s", url, exc)
        return None  # caller will handle fallback
    
def get_trending_movies():
    cache_key = "tmdb:trending:week"
    cached = cache.get(cache_key)
    if cached is not None:
        logger.info("get_trending_movies: cache hit")
        return cached

    logger.info("get_trending_movies: cache miss -> fetching TMDb")
    results = _fetch_from_tmdb("/trending/movie/week")
    if results is None:
        # if TMDb failed, try returning stale cache if available
        stale = cache.get(cache_key)
        return stale or []
    # save to cache
    cache.set(cache_key, results, TRENDING_TTL)
    return results



def get_recommended_movies(movie_id):
    cache_key = f"tmdb:recommendations:{movie_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        logger.info("get_recommended_movies(%s): cache hit", movie_id)
        return cached

    logger.info("get_recommended_movies(%s): cache miss -> fetching TMDb", movie_id)
    results = _fetch_from_tmdb(f"/movie/{movie_id}/recommendations")
    if results is None:
        stale = cache.get(cache_key)
        return stale or []
    cache.set(cache_key, results, RECOMM_TTL)
    return results
