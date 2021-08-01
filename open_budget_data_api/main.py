import logging
import os
from flask import Flask
from flask_cors import CORS

from apisql import apisql_blueprint

app = Flask(__name__)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

MAX_ROWS = int(os.environ.get('MAX_ROWS', 1000))

app.register_blueprint(
    apisql_blueprint(connection_string=os.environ['DATABASE_URL'], max_rows=MAX_ROWS, debug=False),
    url_prefix='/api/'
)
CORS(app)
