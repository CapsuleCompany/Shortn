# Shorten

Core URL shortening app for the Shortn service. Handles creating short URLs, redirecting, listing, and click analytics.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/shorten/` | Create a shortened URL |
| `GET` | `/<short_code>/` | Redirect to the original URL (increments click count) |
| `GET` | `/urls/` | List all shortened URLs (with filtering, search, ordering) |
| `GET` | `/analytics/<short_code>/` | Retrieve analytics for a shortened URL |

The `/urls/` endpoint also supports the full `ModelViewSet` CRUD operations (retrieve, update, delete) via the DRF router.

## Model — `ShortenedURL`

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key (auto-generated) |
| `original_url` | URLField | The original long URL |
| `short_code` | CharField | Unique short code (default length: 6, configurable) |
| `created_at` | DateTimeField | Creation timestamp |
| `click_count` | IntegerField | Number of redirects served |
| `ip_address` | GenericIPAddressField | IP of the creator (optional) |

## Filtering and Search

The list endpoint (`/urls/`) supports:

- `?min_clicks=N` — Filter URLs with at least N clicks
- `?search=term` — Search by `original_url` or `short_code`
- `?ordering=click_count` or `?ordering=-created_at` — Sort results

## Caching

- **Redirects** are cached to avoid DB lookups on repeat visits (TTL: `REDIRECT_CACHE_TTL`, default 5 min)
- **Analytics** responses are cached to reduce load under heavy polling (TTL: `ANALYTICS_CACHE_TTL`, default 30 sec)

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `SHORT_CODE_LENGTH` | `6` | Length of generated short codes |
| `BASE_URL` | `http://localhost:8000` | Base URL used in `short_url` responses |
| `REDIRECT_CACHE_TTL` | `300` | Redirect cache TTL in seconds |
| `ANALYTICS_CACHE_TTL` | `30` | Analytics cache TTL in seconds |

## Module Structure

- `models.py` — `ShortenedURL` model and `generate_short_code()` helper
- `views.py` — `CreateShortURL`, `RedirectShortURL`, `URLAnalytics`, `URLShortenerViewSet`
- `serializers.py` — `ShortenedURLSerializer` (includes computed `short_url` field)
- `urls.py` — Route definitions with DRF router
