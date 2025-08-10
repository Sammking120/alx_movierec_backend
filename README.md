# Movie Recommendation Backend

A Django + DRF backend that serves movie data from TMDb, supports user registration + JWT auth, lets users save favorite movies, and caches popular endpoints using Redis. Swagger UI is available at `/api/docs/`.

---

## Features
- TMDb integration for trending & recommendations
- JWT authentication (djangorestframework-simplejwt)
- Save & manage user favorite movies (CRUD)
- Redis caching for public endpoints (trending/recommendations)
- API docs via drf-spectacular (Swagger UI)
- Ready for Docker-based deployment

---

## Tech stack
- Python 3.11 (or 3.10+)
- Django
- Django REST Framework
- PostgreSQL
- Redis
- drf-spectacular (OpenAPI / Swagger)
- Gunicorn (production WSGI)
- Docker + docker-compose (recommended for local dev)

---

## Quickstart — Local (without Docker)

1. Create a virtualenv and install deps:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

---


---

## 2) Create `Dockerfile` (multi-stage)

Create file named `Dockerfile` (paste exactly):

```dockerfile
# Stage 1 — build dependencies
FROM python:3.11-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# upgrade pip and install dependencies into a wheel cache
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# Stage 2 — runtime image
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps (runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 curl \
    && rm -rf /var/lib/apt/lists/*

# copy wheels and install
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache /wheels/*

# copy project
COPY . /app

# collectstatic will be run at container start or via docker-compose command
ENV DJANGO_SETTINGS_MODULE=moviex_shop.settings

# Create a non-root user (optional but recommended)
RUN groupadd -r app && useradd -r -g app app
RUN chown -R app:app /app
USER app

# Expose the port
EXPOSE 8000

# Use Gunicorn for production
CMD ["gunicorn", "moviex_shop.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
