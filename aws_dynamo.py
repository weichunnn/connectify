# connect to aws account with boto3
import boto3
import os

from dotenv import load_dotenv

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

def connect_table(table_name):
    table = dynamodb.Table(table_name)

    if table.table_status != "ACTIVE":
        raise Exception("Table is not active")

    return table

# get data from dynamo db
def get_user_tracks(table, id):

    response = table.get_item(Key={"id": id})
    return response["Items"]
