import os

import logging
from datetime import date

from decimal import Decimal
from sqlalchemy import create_engine
from itertools import islice

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

engine = create_engine(os.environ['DATABASE_URL'], pool_size=20, max_overflow=0)
log.info('Attempting connection...')
engine.connect()
log.info('Connection Okay')


def jsonable(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, list):
        return [jsonable(x) for x in obj]
    if isinstance(obj, dict):
        return dict((k, jsonable(v)) for k, v in obj.items())
    return obj


def query_db_streaming(query_str):
    try:
        with engine.connect() as connection:
            log.info('executing %r', query_str)
            result = connection.execution_options(stream_results=True)\
                .execute(query_str)
            yield result.keys()
            yield from map(jsonable,
                           map(dict, result))
    except Exception:
        log.exception('EXC')
        raise


def query_db(query_str):
    try:
        with engine.connect() as connection:
            query = "select * from (%s) s limit 100" % query_str
            count_query = "select count(1) from (%s) s" % query_str
            log.info('executing %r', count_query)
            count = connection.execute(count_query).fetchone()[0]
            log.info('count %r', count)
            log.info('executing %r', query)
            result = connection.execute(query)
            rows = list(map(dict, islice(iter(result), 0, 1000)))
            rows = [jsonable(row) for row in rows]
            log.info('rowcount %r', len(rows))
    except Exception:
        log.exception('EXC')
        raise
    return {'total': count,
            'rows': rows,
            }
