# Shrink

A simple, self-hosted URL shortener.

## Features

- Create short URLs
- Redirect from short to long URL
- Delete short URLs
- Click analytics (planned)

## Usage

```bash
pip install -r requirements.txt
python app.py
```

### API

```
POST /shorten    {"url": "https://example.com"}  → {"short": "abc123", "url": "http://localhost:8000/abc123"}
GET  /:code      → 302 redirect to original URL
DELETE /:code    → deletes the short URL
GET  /stats      → (coming soon)
```
