from django.conf import settings
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyClient:
    def __init__(self):
        self.client = Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=settings.SPOTIFY_CLIENT_ID,
                client_secret=settings.SPOTIFY_CLIENT_SECRET
            )
        )

    def search_by_track(self, track):
        return self.client.search(
            q=track
        )
