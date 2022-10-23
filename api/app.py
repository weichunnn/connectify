import json
from aws_dynamo import connect_table
from flask import Flask, session, request, redirect
from flask_session import Session
import spotipy
from decimal import Decimal
import os
from dotenv import load_dotenv
from functools import wraps
import pandas as pd
import json
from sklearn.cluster import KMeans
import pandas as pd
from flask_cors import CORS
import boto3
from boto3.dynamodb.conditions import Key, Attr
import numpy as np

# load env
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print('login checked')
        cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
        # auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
        auth_manager = spotipy.oauth2.SpotifyOAuth()
        # if not auth_manager.validate_token():
        #     return redirect('/login')
        kwargs['spotify'] = spotipy.Spotify(auth_manager=auth_manager)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login')
def index():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing playlist-modify-private user-top-read',
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    if request.args.get("code"):
        # Step 2. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        print('here')
        return redirect('/login')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 1. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return {"redirected": auth_url}
        # return f'<h2><a href="{auth_url}">Sign in</a></h2>'

    # Step 3. Signed in, display data
    # spotify = spotipy.Spotify(auth_manager=auth_manager)
    top()
    regroup_cluster()
    return redirect("http://localhost:3000/recommend", code=302)
    # return 'initialized'

@app.route('/top')
@login_required
def top(spotify):
    print('runned')
    # get top tracks
    top_tracks = spotify.current_user_top_tracks(limit=20, time_range='short_term')
    top_tracks = top_tracks['items']
    track_details = [{"track_id": track['id'], "song_name": track['name']} for track in top_tracks][:5]

    #get id and name for user
    user_id = spotify.me()['id']
    user_name = spotify.me()['display_name']

    # update user table baed on id
    table = connect_table('user_table')
    table.update_item(
        Key={
            'id': user_id
        },
        UpdateExpression="set tracks = :t, #n = :s",
        ExpressionAttributeValues={
            ':t': track_details,
            ':s': user_name
        },
        ExpressionAttributeNames={
            "#n": "name"
        },
        ReturnValues="UPDATED_NEW"
    )

    # extract the ids for the tracks
    track_ids = [track['id'] for track in top_tracks]
    # get the audio features for the tracks
    audio_features = spotify.audio_features(track_ids)
    truncated =  [{"id": track['id'], "acousticness": track['acousticness'], "danceability": track['danceability'], "energy": track['energy'],
    "instrumentalness": track['instrumentalness'], "key": track['key'], "liveness": track['liveness'],
    "loudness": track['loudness'], "mode": track['mode'], 
    "speechiness": track['speechiness'], "tempo": track['tempo'],
    "valence": track['valence']} for track in audio_features]
    
    # convert dict into data frame
    df = pd.DataFrame(truncated)
    average_track = df.mean().reset_index()
    average_track = average_track.rename(columns={'index': 'feature', 0: 'average'})
    # convet avergae track to key value paiurs
    average_track = average_track.to_dict('records')
    average_track = {track['feature']: track['average'] for track in average_track}

    average_track['id'] = spotify.me()['id']
    average_track['user_name'] = spotify.me()['display_name']
    average_track['group_cluster'] = 0
    average_track["score"] = np.random.randint(80, 100)


    average_track = json.loads(json.dumps(average_track), parse_float=Decimal)
    feature_db = connect_table("feature_table")
    feature_db.put_item(Item=average_track)

    return average_track

@app.route('/all_users')
def regroup_cluster():
    # get all rows from featuyre table
    feature_db = connect_table("feature_table")
    response = feature_db.scan()
    mapped = response['Items']
    data = response['Items']
    # get all keys except username
    keys = list(data[0].keys())
    keys.remove('user_name')
    keys.remove('id')
    keys.remove('group_cluster')
    data = pd.DataFrame(data, columns=keys)
    data = data.values.tolist()

    km = KMeans(n_clusters=max(1, len(data) // 10))
    preds = km.fit_predict(data)
    print(preds)
    for i in range(len(mapped)):
        user = mapped[i]
        print(user)
        id = str(user['id'])
        # updated dynamodb based on id
        feature_db.update_item(
            Key={
                'id': id
            },
            UpdateExpression="set group_cluster = :c",
            ExpressionAttributeValues={
                ':c': int(preds[i])
            },
            ReturnValues="UPDATED_NEW"
        )

    return "done"

@app.route('/recommendations')
@login_required
def recommendations(spotify):
    print('bruh')
   # get all id from user table which mathc id = 1
   # get current user id
    user_id = spotify.me()['id']
    # find row in feature table based on id
    feature_db = connect_table("feature_table")
    response = feature_db.get_item(
        Key={
            'id': user_id
        }
    )
    # get the cluster
    user_cluster = response['Item']['group_cluster']
    # get all users in the same cluster
    user_cluster = 0
    response = feature_db.scan(
        FilterExpression=Attr('group_cluster').eq(user_cluster)
    )
     # get all ids
    ids = [user['id'] for user in response['Items']]
    # get all tracks from user table
    table = connect_table('user_table')
    response = table.scan(
        FilterExpression=Attr('id').is_in(ids)
    )
       
    return {"data":response['Items']}
    

@app.route('/sign_out')
def sign_out():
    session.pop("token_info", None)
    return redirect('/')

@app.route('/playlists')
@login_required
def playlists(spotify):
    return spotify.current_user_playlists()

@app.route('/currently_playing')
@login_required
def currently_playing(spotify):
    track = spotify.current_user_playing_track()
    if not track is None:
        return track
    return "No track currently playing."


@app.route('/current_user')
@login_required
def current_user(spotify):
    return spotify.current_user()

if __name__ == '__main__':
    # app.run(threaded=True, debug=True, port=int(os.environ.get("PORT",
    #                                                os.environ.get("SPOTIPY_REDIRECT_URI", 8080).split(":")[-1])))
    app.run(threaded=True, debug=True, port='8080')


# sp = None

# # create route
# @app.route("/auth")
# def index():
#     scope=["user-library-read", "user-top-read"]
#     token, sp = authenticate(scope)
    

# @app.route("/user")
# def haha():
#     users_dict = {}
#      # get user info
#     user = sp.current_user()
#     user_id = user["id"]

#     users_dict["id"] = user_id
#     users_dict["name"] = user["display_name"]
#     users_dict["tracks"] = []

#     tracks_list = users_dict["tracks"]

#     # get user top tracks
#     top_tracks = sp.current_user_top_tracks()

#     # liked_tracks = sp.current_user_saved_tracks()

#     # for res in top_tracks["items"]:
#     #     # get song info
#     #     track_dict = get_song_info(res)
#     #     song_id = track_dict["id"]

#     #     # get song features
#     #     features = sp.audio_features(song_id)

#     #     # add audio features to dict
#     #     track_dict.update(features[0])

#     #     tracks_list.append(track_dict)

#     #     print(f"Track: {track_dict['name']} by {track_dict['artist_name']} added")
#     print(users_dict)

# @app.route("/api/ingest")
# def ingest():
#     spotify_db = connect_table("spotify")
#     users_dict = json.loads(json.dumps(users_dict), parse_float=Decimal)
