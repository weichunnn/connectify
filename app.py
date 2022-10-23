from flask import Flask
from spotify import authenticate

# create flask app
app = Flask(__name__)


# create route
@app.route("/")
def index():
    return authenticate()
