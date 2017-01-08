import logging

from flask_restplus import Resource
from sqlalchemy.sql.expression import func

from open_budget_data_api.api.restplus import api, paginate, page_args, page_of
from open_budget_data_api.api.serializers import support_item
from open_budget_data_api.models import Support

log = logging.getLogger(__name__)

ns = api.namespace('supports', description='The Open Budget API : Supports')


@ns.route('/<code>')
@api.expect(page_args, validate=False)
class SupportCode(Resource):
    @api.marshal_with(page_of(support_item))
    @api.response(404, 'Support item not found.')
    def get(self, code):
        """ Returns supports for code prefix. """
        return paginate(page_args, Support.query.filter(Support.code.like(code + '%')).order_by(Support.year))


@ns.route('/<code>/<int:year>')
@api.expect(page_args, validate=False)
class SupportCodeYear(Resource):
    @api.marshal_with(page_of(support_item))
    @api.response(404, 'Support item not found.')
    def get(self, code, year):
        """ Returns supports for code prefix and year. """
        return paginate(page_args, Support.query.filter(Support.code.like(code + '%'), Support.year == year).order_by(
            Support.recipient, Support.kind, Support.year))


@ns.route('/entity/<entity_id>')
@api.expect(page_args, validate=False)
class SupportEntity(Resource):
    @api.marshal_with(page_of(support_item))
    @api.response(404, 'Support item not found.')
    def get(self, entity_id):
        """ Returns supports for entity. """
        return paginate(page_args, Support.query.filter(Support.entity_id == entity_id).order_by(Support.year.desc))


@ns.route('/recipient/<recipient>')
@api.expect(page_args, validate=False)
class SupportRecipient(Resource):
    @api.marshal_with(page_of(support_item))
    @api.response(404, 'Support item not found.')
    def get(self, recipient):
        """ Returns supports for recipient. """
        raise NotImplementedError


@ns.route('/recipient/<recipient>/<int:year>')
@api.expect(page_args, validate=False)
class SupportRecipientYear(Resource):
    @api.marshal_with(page_of(support_item))
    @api.response(404, 'Support item not found.')
    def get(self, recipient, year):
        """ Returns supports for recipient. """
        raise NotImplementedError


@ns.route('/kind/<kind>')
@api.expect(page_args, validate=False)
class SupportKind(Resource):
    @api.marshal_with(page_of(support_item))
    @api.response(404, 'Support item not found.')
    def get(self, kind):
        """ Returns supports for kind. """
        return paginate(page_args, Support.query.filter(Support.kind == kind))


@ns.route('/kind/<kind>/<code>')
@api.expect(page_args, validate=False)
class SupportKindCode(Resource):
    @api.marshal_with(page_of(support_item))
    @api.response(404, 'Support item not found.')
    def get(self, kind, code):
        """ Returns supports for kind and code prefix. """
        return paginate(page_args, Support.query.filter(Support.kind == kind, Support.code.like(code + '%'),
                                                        func.length(Support.code) == len(code) + 2))


@ns.route('/kind/<kind>/<code>/<int:year>')
@api.expect(page_args, validate=False)
class SupportKindCodeYear(Resource):
    @api.marshal_with(page_of(support_item))
    @api.response(404, 'Support item not found.')
    def get(self, kind, code, year):
        """ Returns supports for kind, code prefix and year. """
        return paginate(page_args,
                        Support.query.filter(Support.kind == kind, Support.year == year, Support.code.like(code + '%'),
                                             func.length(Support.code) == len(code) + 2))

# todo
# @ns.route('/kind/<kind>/<code>/aggregated')
# @ns.route('/kind/<kind>/<code>/<int:year>/aggregated')
