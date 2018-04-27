import csv
import logging.config
import tempfile

import xlsxwriter

from io import StringIO
from flask import Flask, request, abort, Response, send_file
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


@app.route('/api/download') # noqa
def download():
    results = query_db_streaming(request.values.get('query'))
    format = request.values.get('format', 'csv')
    if format not in ('csv', 'xlsx'):
        abort(400)
    mime = {
        'csv': 'text/csv',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }[format]

    if format == 'csv':
        def generate():
            buffer = StringIO()
            try:
                headers = next(results)
            except StopIteration:
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

        headers = {'Content-Type': mime,
                   'Content-Disposition': 'attachment; filename=budgetkey.csv'}
        return Response(generate(),
                        content_type='text/csv', headers=headers)
    if format == 'xlsx':
        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.xslx') as out:
            try:
                workbook = xlsxwriter.Workbook(out.name)
                worksheet = workbook.add_worksheet()
                headers = next(results)
                for j, h in enumerate(headers):
                    worksheet.write(0, j, h)
                for i, row in enumerate(results):
                    for j, h in enumerate(headers):
                        v = row.get(h)
                        if v is not None:
                            worksheet.write(i+1, j, v)
            finally:
                workbook.close()
            return send_file(out.name, mimetype=mime, as_attachment=True, attachment_filename='budgetkey.xlsx')


initialize_app(app)
logging.error('Initialized App')
