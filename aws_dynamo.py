# connect to aws account with boto3
import boto3
import os

from dotenv import load_dotenv

from pprint import pprint
import json
from decimal import Decimal

from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import names

import random 
import string

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

def connect_table(table_name):
    table = dynamodb.Table(table_name)

    if table.table_status != "ACTIVE":
        raise Exception("Table is not active")

    return table

# get data from dynamo db
def get_user_tracks(table, id):

    response = table.get_item(Key={"id": id})
    return response["Items"]


    

if __name__ == "__main__":
    df = pd.read_csv("data.csv")
    np.random.seed(200)
    df = df.sample(n=400)
    df = df.reset_index(drop=True)

    fake_names = [names.get_full_name() for _ in range(20)]
    fake_ids = [i for i in range(20)]

    df["id"] = np.random.choice(fake_ids, size=len(df))
    df["user_name"] = df["id"].apply(lambda x : fake_names[x])

    song_features = df.iloc[:, 9:20]

    user_features = song_features.groupby(df["id"]).mean().reset_index()
    user_features["user_name"] = user_features["id"].apply(lambda x : fake_names[x])

    X = user_features.iloc[:, 1:11].values

    km = KMeans(n_clusters=max(1, len(X) // 10))
    preds = km.fit_predict(X)

    user_features["cluster"] = preds

    user_features_dict = user_features.to_dict('records')

    feature_db = connect_table("feature_table")


    ## ingest into dynamodb
    #for user in user_features_dict:
    #    user = json.loads(json.dumps(user), parse_float=Decimal)

    #    print("ingesting ", user["user_name"])
    #    feature_db.put_item(
    #        Item=user
    #    )

    
    user_grp = df.groupby("id").apply(lambda x : x.sample(n=5))
    df = user_grp.reset_index(drop=True)

    user_list = []
    for i in range(len(user_features)):
        temp_d = {}
        user_id = user_features.iloc[i]["id"]
        temp_d["id"] = user_id
        temp_d["name"] = user_features.iloc[i]["user_name"]
        temp_d["tracks"] = df[df["id"] == user_id][['id', 'name']].to_dict('records')
        user_list.append(temp_d)

    class NpEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.integer):
                return int(obj)
            if isinstance(obj, np.floating):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return super(NpEncoder, self).default(obj)

    feature_db = connect_table("user_table")

    for user in user_list:
        user = json.loads(json.dumps(user, cls=NpEncoder), parse_float=Decimal)

        print("ingesting ", user["name"])
        feature_db.put_item(
            Item=user
        )