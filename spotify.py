import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import os
from dotenv import load_dotenv

from pprint import pprint

load_dotenv()


def authenticate(scope):

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            cache_handler=None,
            scope=scope,
        )
    )

    # get access token
    token = sp.auth_manager.get_access_token(as_dict=False)

    return sp


def get_artist_albums(sp: spotipy.Spotify, artist_uri: str):

    results = sp.artist_albums(artist_uri, album_type="album")
    albums = results["items"]
    while results["next"]:
        results = sp.next(results)
        albums.extend(results["items"])

    for album in albums:
        print(album["name"])


def get_song_info(res):
    res_dict = {
        "name": res["name"],
        "song_uri": res["uri"],
        "id": res["id"],
        "url": res["external_urls"]["spotify"],
        "album_name": res["album"]["name"],
        "artist_name": res["artists"][0]["name"],
    }

    return res_dict


if __name__ == "__main__":

    # reads from .cache
    sp = authenticate(scope=["user-library-read", "user-top-read"])
    # sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    users_dict = {}

    # get user info
    user = sp.current_user()
    user_id = user["id"]

    users_dict["id"] = user_id
    users_dict["name"] = user["display_name"]
    users_dict["tracks"] = []

    tracks_list = users_dict["tracks"]

    # get user top tracks
    top_tracks = sp.current_user_top_tracks()

    # liked_tracks = sp.current_user_saved_tracks()

    track_dict = {
        "album_name": "Harry's House",
        "artist_name": "Harry Styles",
        "id": "51Zw1cKDgkad0CXv23HCMU",
        "name": "Daylight",
        "url": "https://open.spotify.com/track/51Zw1cKDgkad0CXv23HCMU",
    }

    for res in top_tracks["items"]:
        # get song info
        track_dict = get_song_info(res)
        song_id = track_dict["id"]

        # get song features
        features = sp.audio_features(song_id)

        # add audio features to dict
        track_dict.update(features[0])

        tracks_list.append(track_dict)

        print(f"Track: {track_dict['name']} by {track_dict['artist_name']} added")
