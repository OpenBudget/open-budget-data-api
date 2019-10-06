import os
import re

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


def formatter(mod): #noqa
    if mod == 'number':
        def _f(x, row):
            return str(x)
        return _f
    elif mod == 'budget_code':
        def _f(x, row):
            x = x[2:]
            code = ''
            while len(x) > 0:
                code += '.' + x[:2]
                x = x[2:]
            return code[1:]
        return _f
    elif mod == 'yesno':
        def _f(x, row):
            return 'כן' if x else 'לא'
        return _f
    elif mod.startswith('item_link('):
        # param = mod.split('(')[1][:-1]

        def _f(x, row):
            # TODO: Restore link at some point?
            # if row.get(param):
            #     return '{} [https://next.obudget.org/i/{}]'.format(x, row[param])
            # else:
            return x
        return _f
    elif mod.startswith('search_term('):
        # param = mod.split('(')[1][:-1]

        def _f(x, row):
            # TODO: Restore link at some point?
            # if row.get(param):
            #     return '{} [https://next.obudget.org/s/?q={}]'.format(x, row[param])
            # else:
            return x
        return _f


def compose(f, g):
    def _f(x, row):
        return g(f(x, row), row)
    return _f


def getter(h):
    hdr = h

    def _f(x, row):
        return row[hdr]
    return _f


def wrapper(f):

    def _f(row):
        return f('', row)
    return _f


PARAM = re.compile(':([a-z()_]+)$')


def parse_formatters(formatters):
    _headers = []
    _formatters = []
    for h in formatters:
        matches = PARAM.findall(h)
        funcs = []
        while len(matches) > 0:
            mod = matches[0]
            h = h[:-(len(mod)+1)]
            funcs.append(formatter(mod))
            matches = PARAM.findall(h)
        f = getter(h)
        for g in reversed(funcs):
            f = compose(f, g)
        k = wrapper(f)
        _formatters.append(k)
        _headers.append(h)
    return _headers, _formatters


def query_db_streaming(query_str, formatters):
    try:
        headers, formatters = parse_formatters(formatters)

        with engine.connect() as connection:
            log.info('executing %r', query_str)
            result = connection.execution_options(stream_results=True)\
                .execute(query_str)
            yield headers
            yield from (
                [f(row) for f in formatters]
                for row in map(jsonable, map(dict, result))
            )
    except Exception:
        log.exception('EXC')
        raise


def query_db(query_str, max_rows=100):
    try:
        with engine.connect() as connection:
            query = "select * from (%s) s limit %s" % (query_str, max_rows)
            count_query = "select count(1) from (%s) s" % query_str
            log.info('executing %r', count_query)
            count = connection.execute(count_query).fetchone()[0]
            log.info('count %r', count)
            log.info('executing %r', query)
            result = connection.execute(query)
            rows = list(map(dict, islice(iter(result), 0, max_rows)))
            rows = [jsonable(row) for row in rows]
            log.info('rowcount %r', len(rows))
    except Exception:
        log.exception('EXC')
        raise
    return {'total': count,
            'rows': rows,
            }
