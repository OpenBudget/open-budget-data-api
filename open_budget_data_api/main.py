import logging.config

from flask import Flask, request
from flask_jsonpify import jsonpify
from flask_cors import CORS

from .db import query_db

app = Flask(__name__)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def initialize_app(flask_app):
    CORS(flask_app)

    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    flask_app.logger.handlers.extend(gunicorn_error_logger.handlers)


@app.route('/api/query')
def query():
    results = query_db(request.values.get('query'))
    return jsonpify(results)


initialize_app(app)
logging.error('Initialized App')
