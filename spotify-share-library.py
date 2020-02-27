#!/usr/bin/env python3

from aiohttp import web
from datetime import datetime
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
        return web.HTTPFound(url)

async def callback(request):
    async with spotify.Client(CLIENT_ID, CLIENT_SECRET) as client:
        user = await spotify.User.from_code(
            client=client,
            code=request.query['code'],
            redirect_uri=REDIRECT_URI,
            )
    display_name = user.display_name or user.id
    public_library = "%s' Public library" % display_name
    for playlist in await user.get_all_playlists():
        if playlist.name == public_library:
            break
    else:
        playlist = await user.create_playlist(public_library)
    tracks = await user.library.get_all_tracks()
    await playlist.replace_tracks(*tracks)
    return web.HTTPFound(playlist.url)

app = web.Application()
app.add_routes([
    web.get('/', auth),
    web.get('/callback', callback),
])

if __name__ == '__main__':
    web.run_app(app)

