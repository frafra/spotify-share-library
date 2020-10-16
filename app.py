#!/usr/bin/env python3

from starlette.applications import Starlette
from starlette.responses import RedirectResponse
from starlette.routing import Route

import os
import spotify

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = os.environ['REDIRECT_URI']

async def auth(request):
    async with spotify.Client(CLIENT_ID, CLIENT_SECRET) as client:
        url = client.oauth2_url(
            redirect_uri=REDIRECT_URI,
            scopes=['user-library-read', 'playlist-modify-public'])
        return RedirectResponse(url)

async def callback(request):
    async with spotify.Client(CLIENT_ID, CLIENT_SECRET) as client:
        user = await spotify.User.from_code(
            client=client,
            code=request.query_params['code'],
            redirect_uri=REDIRECT_URI,
            )
    display_name = user.display_name or user.id
    public_library = "%s's Public library" % display_name
    for playlist in await user.get_all_playlists():
        if playlist.name == public_library:
            break
    else:
        playlist = await user.create_playlist(public_library)
    tracks = await user.library.get_all_tracks()
    await playlist.replace_tracks(*tracks)
    return RedirectResponse(playlist.url)

routes = [
    Route('/', endpoint=auth),
    Route('/callback', endpoint=callback),
]

main = Starlette(os.environ.get('DEBUG', False), routes=routes)
