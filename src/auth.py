import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


def get_spotify_client():
    load_dotenv()
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URI = "http://127.0.0.1:80"

    SCOPE = "playlist-modify-private playlist-modify-public user-library-read"

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            cache_path=".cache-spotify",
        )
    )

    return sp
