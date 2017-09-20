import os

import logging
from sqlalchemy import create_engine
from itertools import islice

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

engine = create_engine(os.environ['DATABASE_URL'], pool_size=20, max_overflow=0)
log.info('Attempting connection...')
engine.connect()
log.info('Connection Okay')


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
            log.info('rowcount %r', len(rows))
    except:
        log.exception('EXC')
        raise
    return {'total': count,
            'rows': rows,
            }
