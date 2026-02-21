# Auth

JWT authentication app for the Shortn service. Provides user registration and token-based login using [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/).

## Endpoints

All routes are mounted under `/auth/`.

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/auth/register/` | Register a new user (username, email, password) |
| `POST` | `/auth/login/` | Obtain a JWT access/refresh token pair |
| `POST` | `/auth/refresh/` | Refresh an expired access token |

## Registration

```bash
curl -X POST http://localhost:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com", "password": "secret123"}'
```

Passwords must be at least 6 characters.

## Login

```bash
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret123"}'
```

Returns `access` and `refresh` tokens.

## Configuration

Token lifetimes are controlled via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `JWT_ACCESS_TOKEN_LIFETIME_DAYS` | `1` | Access token lifetime in days |
| `JWT_REFRESH_TOKEN_LIFETIME_DAYS` | `7` | Refresh token lifetime in days |
| `JWT_SECRET_KEY` | `SECRET_KEY` | Signing key for tokens |

## Module Structure

- `views.py` — `RegisterView` (CreateAPIView)
- `serializers.py` — `RegisterSerializer` (validates and creates users)
- `urls.py` — Route definitions
