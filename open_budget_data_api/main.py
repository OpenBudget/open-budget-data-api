import csv
import logging.config

from io import StringIO
from flask import Flask, request
from flask import Response
from flask_jsonpify import jsonpify
from flask_cors import CORS

from .db import query_db, query_db_streaming

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


@app.route('/api/download')
def download():
    results = query_db_streaming(request.values.get('query'))
    headers = {'Content-Type': 'text/csv',
               'Content-Disposition': 'attachment; filename=budgetkey.csv'}

    def generate():
        buffer = StringIO()
        try:
            headers = next(results)
        except:
            return
        writer = csv.DictWriter(buffer, headers)
        writer.writeheader()
        for row in results:
            writer.writerow(row)
            pos = buffer.tell()
            buffer.seek(0)
            ret = buffer.read(pos)
            buffer.seek(0)
            yield ret

    return Response(generate(),
                    content_type='text/csv', headers=headers)

initialize_app(app)
logging.error('Initialized App')
