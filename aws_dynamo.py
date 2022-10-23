# connect to aws account with boto3
import boto3
import os

from dotenv import load_dotenv
import json
from decimal import Decimal
from pprint import pprint


load_dotenv()

aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
aws_session_token = os.environ["AWS_SESSION_TOKEN"]


# add credentials to boto3
dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
)


# get data from dynamo db
def get_data(table):

    response = table.scan()
    return response["Items"]


if __name__ == "__main__":

    dynamodb.get_available_subresources()

    table = dynamodb.Table("spotify")
    print(table.table_status)

    users_dict = {
        "id": "31w6rspp4fe5ihwoimt4of5tcwiu",
        "name": "Ben",
        "songs": [
            {
                "51Zw1cKDgkad0CXv23HCMU": {
                    "acousticness": 0.484,
                    "album_name": "Harry's House",
                    "analysis_url": "https://api.spotify.com/v1/audio-analysis/51Zw1cKDgkad0CXv23HCMU",
                    "artist_name": "Harry Styles",
                    "danceability": 0.686,
                    "duration_ms": 164533,
                    "energy": 0.445,
                    "id": "51Zw1cKDgkad0CXv23HCMU",
                    "instrumentalness": 0.00144,
                    "key": 0,
                    "liveness": 0.175,
                    "loudness": -7.189,
                    "mode": 1,
                    "name": "Daylight",
                    "speechiness": 0.0398,
                    "tempo": 145.5,
                    "time_signature": 3,
                    "track_href": "https://api.spotify.com/v1/tracks/51Zw1cKDgkad0CXv23HCMU",
                    "type": "audio_features",
                    "uri": "spotify:track:51Zw1cKDgkad0CXv23HCMU",
                    "url": "https://open.spotify.com/track/51Zw1cKDgkad0CXv23HCMU",
                    "valence": 0.626,
                }
            }
        ],
    }
    users_dict = json.loads(json.dumps(users_dict), parse_float=Decimal)

    # table.put_item(Item=users_dict)

    res = table.get_item(Key={"id": "31w6rspp4fe5ihwoimt4of5tcwiu"})
