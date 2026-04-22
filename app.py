#!/usr/bin/env python3

from itertools import batched

import environ
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from starlette.applications import Starlette
from starlette.responses import RedirectResponse
from starlette.routing import Route

env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env()

CLIENT_ID = env("CLIENT_ID")
CLIENT_SECRET = env("CLIENT_SECRET")
SCOPES = "user-library-read playlist-modify-public"


def get_redirect_uri(request):
    scheme = request.headers.get("x-forwarded-proto", request.url.scheme)
    host = request.headers.get("host", request.url.netloc)
    return f"{scheme}://{host}/callback"


def get_oauth(request):
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=get_redirect_uri(request),
        scope=SCOPES,
    )


async def auth(request):
    url = get_oauth(request).get_authorize_url()
    return RedirectResponse(url)


async def callback(request):
    sp_oauth = get_oauth(request)
    token_info = sp_oauth.get_access_token(request.query_params["code"], as_dict=False)
    sp = spotipy.Spotify(auth=token_info)

    user = sp.current_user()
    display_name = user.get("display_name") or user["id"]
    public_library = "%s's Public library" % display_name

    playlist_id = None
    playlists = sp.current_user_playlists()
    while playlists:
        for playlist in playlists["items"]:
            if playlist["name"] == public_library:
                playlist_id = playlist["id"]
                break
        if playlist_id or not playlists["next"]:
            break
        playlists = sp.next(playlists)

    if not playlist_id:
        playlist = sp.current_user_playlist_create(public_library)
        playlist_id = playlist["id"]

    track_uris = []
    results = sp.current_user_saved_tracks()
    while results:
        track_uris.extend(item["track"]["uri"] for item in results["items"])
        if not results["next"]:
            break
        results = sp.next(results)

    chunks = list(batched(track_uris, 100))
    sp.playlist_replace_items(playlist_id, chunks[0] if chunks else [])
    for chunk in chunks[1:]:
        sp.playlist_add_items(playlist_id, chunk)

    return RedirectResponse(f"https://open.spotify.com/playlist/{playlist_id}")


routes = [
    Route("/", endpoint=auth),
    Route("/callback", endpoint=callback),
]

main = Starlette(env("DEBUG"), routes=routes)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(main, host="0.0.0.0", port=8000)
