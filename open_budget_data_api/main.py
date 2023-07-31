import logging
import os
from flask import Flask
from flask_cors import CORS
from flask_caching import Cache

from apisql import apisql_blueprint

config = {
    "CACHE_TYPE": "FileSystemCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 600,
    "CACHE_DIR": ".cache",
    "CACHE_THRESHOLD": 100,
    "CACHE_OPTIONS": {
        "mode": 0o700
    },
}
cache = Cache(config=config)

app = Flask(__name__)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

MAX_ROWS = int(os.environ.get('MAX_ROWS', 1000))

app.register_blueprint(
    apisql_blueprint(connection_string=os.environ['DATABASE_URL'], max_rows=MAX_ROWS, debug=False, cache=cache),
    url_prefix='/api/'
)
CORS(app)
cache.init_app(app)

@app.after_request
def add_header(response):
    response.cache_control.max_age = 600
    return response
