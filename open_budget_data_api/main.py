import csv
import logging.config
import tempfile
import urllib
import os
import xlsxwriter

from io import StringIO
from flask import Flask, request, abort, Response, send_file
from flask_jsonpify import jsonpify
from flask_cors import CORS

from .db import query_db, query_db_streaming

app = Flask(__name__)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

MAX_ROWS = int(os.environ.get('MAX_ROWS', 100))


def initialize_app(flask_app):
    CORS(flask_app)

    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    flask_app.logger.handlers.extend(gunicorn_error_logger.handlers)

def detect_bot():
    if request.user_agent.browser in ('google', 'aol', 'baidu', 'bing', 'yahoo'):
        log.info('Bot detected %s: %s', request.user_agent.string, request.user_agent.browser)
    elif any(x in request.user_agent.string.lower() for x in ('applebot', 'yandexbot')):
        log.info('Bot detected %s: %s', request.user_agent.string, request.user_agent.browser)
    else:
        return False
    return True

@app.route('/api/query')
def query():
    results = dict(total=0, rows=[])
    if not detect_bot():
        num_rows = int(request.values.get('num_rows', MAX_ROWS))
        num_rows = min(num_rows, MAX_ROWS)
        results = query_db(request.values.get('query'), max_rows=num_rows)
    return jsonpify(results)


@app.route('/api/download') # noqa
def download():
    format = request.values.get('format', 'csv')

    file_name = request.values.get('filename')
    # Create a default value here in case this parameter is not provided
    if file_name is None:
        file_name = 'budgetkey'

    formatters = request.values.get('headers').split(';')

    if format not in ('csv', 'xlsx'):
        abort(400)

    if detect_bot():
        headers = {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=bot-detected.csv'
        }
        return Response('',
                        content_type='text/csv', headers=headers)

    mime = {
        'csv': 'text/csv',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }[format]
    results = query_db_streaming(request.values.get('query'), formatters)

    if format == 'csv':
        def generate():
            buffer = StringIO()
            writer = csv.writer(buffer)
            for row in results:
                writer.writerow(row)
                pos = buffer.tell()
                buffer.seek(0)
                ret = buffer.read(pos)
                buffer.seek(0)
                yield ret

        # Encode the filename in utf-8 and url encoding
        file_name_utf8_encoded = file_name.encode('utf-8')
        file_name_url_encoded = urllib.parse.quote(file_name_utf8_encoded)

        headers = {
            'Content-Type': mime,
            'Content-Disposition': 'attachment; filename=' + file_name_url_encoded + '.csv'
        }
        return Response(generate(),
                        content_type='text/csv', headers=headers)
    if format == 'xlsx':
        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.xslx') as out:
            try:
                workbook = xlsxwriter.Workbook(out.name)
                worksheet = workbook.add_worksheet()
                for i, row in enumerate(results):
                    for j, v in enumerate(row):
                        if v is not None:
                            try:
                                worksheet.write_number(i, j, float(v))
                            except ValueError:
                                worksheet.write(i, j, str(v))
            finally:
                workbook.close()
            return send_file(out.name, mimetype=mime, as_attachment=True, attachment_filename=file_name + '.xlsx')


initialize_app(app)
logging.error('Initialized App')
