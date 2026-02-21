# QR

QR code generation app for the Shortn service. Generates QR code images from URLs with optional logo overlay.

## Endpoint

Mounted under `/qr/`.

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/qr/generate/` | Generate a QR code PNG for a given URL |

## Usage

### Basic QR code

```bash
curl -X POST http://localhost:8000/qr/generate/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' \
  --output qr.png
```

### QR code with logo

```bash
curl -X POST http://localhost:8000/qr/generate/ \
  -F "url=https://example.com" \
  -F "logo=@logo.png" \
  --output qr.png
```

The logo is resized to 1/4 of the QR code dimensions and centered. High error correction (`ERROR_CORRECT_H`) is used so the code remains scannable with the logo overlay.

## Response

Returns the QR code as a `image/png` response with `Content-Disposition: inline`.

## Model

The `QRCode` model stores:

- `url` — The encoded URL
- `qr_code_image` — The generated image (uploaded to `qr_codes/`)
- `created_at` — Timestamp

## Dependencies

- [qrcode](https://pypi.org/project/qrcode/) — QR code generation
- [Pillow](https://pypi.org/project/Pillow/) — Image processing and logo overlay

## Module Structure

- `views.py` — `GenerateQRCodeView` (accepts JSON or multipart form data)
- `models.py` — `QRCode` model
- `urls.py` — Route definitions
