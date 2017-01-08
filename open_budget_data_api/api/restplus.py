import logging
import traceback

from flask import request
from flask_restplus import Api
from flask_restplus import fields
from flask_restplus import reqparse
from flask_sqlalchemy import Model
from sqlalchemy.orm.exc import NoResultFound

from open_budget_data_api import config

log = logging.getLogger(__name__)

api = Api(endpoint='api',
          version='1.0',
          title='The Open Budget API',
          description='The Open Budget API, powered by Flask RestPlus')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not config.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404


page_args = reqparse.RequestParser()
page_args.add_argument('page', type=int, required=False, default=1, help='Page number')
page_args.add_argument('per_page', type=int, required=False, choices=[2, 10, 20, 30, 40, 50, 100, 200],
                       default=10, help='Results per page {error_msg}')

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})


def page_of(item):
    return api.inherit('Page of ' + item.name, pagination, {
        'items': fields.List(fields.Nested(item))
    })


# todo paginate via interceptor ~ @paginate(
def paginate(pagination_arguments, query):
    args = pagination_arguments.parse_args(request)
    pagination = query.paginate(args.get('page', 1), args.get('per_page', 10), False)
    if len(pagination.items) > 0:
        if not isinstance(pagination.items[0], Model):
            pagination.items = list(map(lambda x: x._asdict(), pagination.items))
    return pagination
