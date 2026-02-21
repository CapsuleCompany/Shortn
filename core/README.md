# core

Django project configuration for the Shortn service. Contains settings, root URL routing, and WSGI/ASGI entry points.

## Root Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | API info with version and endpoint listing |
| `GET` | `/health/` | Health check (returns `{"status": "healthy"}`) |

## URL Routing

All app routes are included from the root URL config:

- `/auth/*` — `Auth.urls`
- `/qr/*` — `QR.urls`
- `/shorten/`, `/urls/`, `/<short_code>/`, `/analytics/*` — `Shorten.urls`

## Settings Overview

Key configuration areas in `settings.py`:

- **Database** — PostgreSQL when `DB_NAME` is set, otherwise SQLite
- **Cache** — Redis when `REDIS_URL` is set, otherwise in-memory (`LocMemCache`)
- **JWT** — Token lifetimes and signing key via `SIMPLE_JWT`
- **REST Framework** — JWT auth, rate limiting, pagination (25 per page), JSON renderer
- **CORS** — Configurable allowed origins via `CORS_ALLOWED_ORIGINS`
- **Static files** — Served via WhiteNoise with compressed manifest storage

## Module Structure

- `settings.py` — All Django and third-party configuration
- `urls.py` — Root URL config, health check, and API info views
- `wsgi.py` — WSGI application entry point
- `asgi.py` — ASGI application entry point
