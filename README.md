# Shortn

A reusable URL shortening microservice built with Django REST Framework. Shorten URLs, track clicks, generate QR codes, and authenticate users — all through a clean JSON API.

## Features

- **URL Shortening** — Generate short, unique links with configurable code length
- **Click Analytics** — Track how many times each link is accessed
- **QR Code Generation** — Create QR codes for any URL, with optional logo overlay
- **JWT Authentication** — Register, login, and refresh tokens
- **Rate Limiting** — Configurable throttling for anonymous and authenticated users
- **CORS Support** — Ready for cross-origin consumption by frontends or other services
- **Docker Ready** — One-command deployment with Docker Compose (PostgreSQL included)
- **Health Check** — `GET /health/` for load balancer and orchestrator probes

## Quick Start

### Local Development

```bash
# Clone and enter the repo
git clone https://github.com/CapsuleCompany/Shortn.git
cd Shortn

# Install dependencies
poetry install

# Copy environment config
cp .env.example .env

# Run migrations and start the server
python manage.py migrate
python manage.py runserver
```

The API is now live at `http://localhost:8000`.

### Docker Compose (PostgreSQL)

```bash
cp .env.example .env
docker compose up --build
```

This starts the API on port `8000` backed by PostgreSQL on port `5432`.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | API info and endpoint listing |
| `GET` | `/health/` | Health check |
| `POST` | `/shorten/` | Create a shortened URL |
| `GET` | `/<short_code>/` | Redirect to original URL |
| `GET` | `/urls/` | List all shortened URLs |
| `GET` | `/analytics/<short_code>/` | Get click analytics for a URL |
| `POST` | `/qr/generate/` | Generate a QR code for a URL |
| `POST` | `/auth/register/` | Register a new user |
| `POST` | `/auth/login/` | Get JWT token pair |
| `POST` | `/auth/refresh/` | Refresh an access token |

### Shorten a URL

```bash
curl -X POST http://localhost:8000/shorten/ \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://example.com/very/long/path"}'
```

Response:

```json
{
  "id": "a1b2c3d4-...",
  "original_url": "https://example.com/very/long/path",
  "short_code": "Xk9mPq",
  "short_url": "http://localhost:8000/Xk9mPq/",
  "created_at": "2025-01-15T12:00:00Z",
  "click_count": 0
}
```

### Get Analytics

```bash
curl http://localhost:8000/analytics/Xk9mPq/
```

### Generate a QR Code

```bash
curl -X POST http://localhost:8000/qr/generate/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' \
  --output qr.png
```

### List URLs with Filtering

```bash
# All URLs
curl http://localhost:8000/urls/

# Filter by minimum clicks
curl http://localhost:8000/urls/?min_clicks=10

# Search by URL or short code
curl http://localhost:8000/urls/?search=example

# Order by click count
curl http://localhost:8000/urls/?ordering=-click_count
```

## Configuration

All configuration is done through environment variables (or a `.env` file). See `.env.example` for the full list.

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | dev-only key | Django secret key |
| `DEBUG` | `False` | Enable debug mode |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated allowed hosts |
| `DB_ENGINE` | `django.db.backends.sqlite3` | Database backend |
| `DB_NAME` | `db.sqlite3` | Database name |
| `DB_USER` | | Database user (PostgreSQL) |
| `DB_PASSWORD` | | Database password (PostgreSQL) |
| `DB_HOST` | `localhost` | Database host |
| `DB_PORT` | `5432` | Database port |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000,...` | Allowed CORS origins |
| `CORS_ALLOW_ALL_ORIGINS` | `False` | Allow all CORS origins |
| `JWT_SECRET_KEY` | `SECRET_KEY` | JWT signing key |
| `JWT_ACCESS_TOKEN_LIFETIME_DAYS` | `1` | Access token lifetime |
| `JWT_REFRESH_TOKEN_LIFETIME_DAYS` | `7` | Refresh token lifetime |
| `SHORT_CODE_LENGTH` | `6` | Length of generated short codes |
| `ANON_RATE_LIMIT` | `60/min` | Rate limit for anonymous users |
| `USER_RATE_LIMIT` | `120/min` | Rate limit for authenticated users |
| `BASE_URL` | `http://localhost:8000` | Base URL used in `short_url` responses |

## Running Tests

```bash
python manage.py test
```

## Production Deployment

1. Set `DEBUG=False` and a strong `SECRET_KEY` in your `.env`
2. Set `ALLOWED_HOSTS` to your domain
3. Use PostgreSQL by setting `DB_ENGINE=django.db.backends.postgresql`
4. Set `BASE_URL` to your public domain (e.g., `https://sho.rt`)
5. Deploy with Docker Compose or behind a reverse proxy with gunicorn:

```bash
gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

## Project Structure

```
Shortn/
├── core/            # Django project settings and root URL config
├── Shorten/         # URL shortening app (models, views, serializers)
├── Auth/            # JWT authentication app
├── QR/              # QR code generation app
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── .env.example
└── pyproject.toml
```

## License

MIT
