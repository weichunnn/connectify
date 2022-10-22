
import spotipy
from spotipy.oauth2 import SpotifyOAuth,SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

def authenticate():
  scope = "user-library-read"
  sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
    scope=scope))

  # get access token
  token = sp.auth_manager.get_access_token(as_dict=False)
  print(token)
  results = sp.current_user_saved_tracks()
  for idx, item in enumerate(results['items']):
      track = item['track']
      print(idx, track['artists'][0]['name'], " – ", track['name'])


def test():
  birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
  spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

  results = spotify.artist_albums(birdy_uri, album_type='album')
  albums = results['items']
  while results['next']:
      results = spotify.next(results)
      albums.extend(results['items'])

  for album in albums:
      print(album['name'])