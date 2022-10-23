from aws_dynamo import connect_table
from flask import Flask
from spotify import authenticate
import json
from decimal import Decimal

# create flask app
app = Flask(__name__)


# create route
@app.route("/")
def index():
    return authenticate()

@app.route("api/ingest")
def ingest():

    spotify_db = connect_table("spotify")
    users_dict = json.loads(json.dumps(users_dict), parse_float=Decimal)