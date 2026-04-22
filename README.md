# Spotify Share Library

Keep your Spotify library synced with a shareable public playlist.

When you visit the app, it authenticates with your Spotify account, creates (or updates) a playlist called "_Your Name_'s Public library", and populates it with all your saved tracks.

**Demo:** [spotify-share-library.fly.dev](https://spotify-share-library.fly.dev/)

## Setup

1. Create an app on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Add your redirect URI (e.g. `http://127.0.0.1:8000/callback`) in the app settings
3. Copy `env.template` to `.env` and fill in your credentials:


| Variable | Description |
|---|---|
| `CLIENT_ID` | Your Spotify app's Client ID |
| `CLIENT_SECRET` | Your Spotify app's Client Secret |
| `DEBUG` | Enable debug mode (default: `false`) |

## Running locally

```sh
uv run uvicorn app:main --host 0.0.0.0
```

Then open http://127.0.0.1:8000.

## Docker

```sh
docker build -t spotify-share-library .
docker run -p 8000:8000 --env-file .env spotify-share-library
```

## Development

Install dev dependencies and set up Git hooks:

```sh
uv sync
prek install
```

## Notes

- A [Spotify Premium](https://www.spotify.com/premium/) account is required for the app owner (Development Mode restriction since February 2026)
- Development Mode apps are limited to 5 users
