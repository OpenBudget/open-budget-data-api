import logging

from flask_restplus import Resource

from open_budget_data_api.api.restplus import api, paginate, page_args, page_of
from open_budget_data_api.api.serializers import changes_item
from open_budget_data_api.models import Changes

log = logging.getLogger(__name__)

ns = api.namespace('changes', description='The Open Budget API : Changes')


@ns.route('/<code>')
@api.expect(page_args, validate=False)
class ChangesCode(Resource):
    @api.marshal_with(page_of(changes_item))
    @api.response(404, 'Changes not found.')
    def get(self, code):
        """ Returns changes for code """
        return paginate(page_args, Changes.query.filter(Changes.budget_code == code).order_by(
            Changes.year.desc(), Changes.date.desc()))


@ns.route('/<code>/<int:year>')
@api.expect(page_args, validate=False)
class ChangesCodeYear(Resource):
    @api.marshal_with(page_of(changes_item))
    @api.response(404, 'Changes not found.')
    def get(self, code, year):
        """ Returns changes for code and year """
        return paginate(page_args, Changes.query.filter(Changes.budget_code == code, Changes.year == year).order_by(
            Changes.year.desc(), Changes.date.desc()))


@ns.route('/<int:leading_item>/<int:req_code>/<int:year>')
@api.expect(page_args, validate=False)
class ChangesLeadingReqYear(Resource):
    @api.marshal_with(page_of(changes_item))
    @api.response(404, 'Changes not found.')
    def get(self, leading_item, req_code, year):
        """ Returns changes by leading item, required code and year """
        return paginate(page_args, Changes.query.filter(
            Changes.leading_item == leading_item, Changes.req_code == req_code, Changes.year == year).order_by(
            Changes.date.desc()))

# todo
# @ns.route('/pending/all')
# class EntityCode(Resource):
#     @api.marshal_with(entity_item)
#     @api.response(404, 'Changes not found.')
#     def get(self):
#         """ Returns changes by leading item, required code and year """
#         return Changes.query.filter(Changes.change_type_id == leading_item, Changes.req_code == req_code,
#                                     Changes.year == year).order_by(Changes.date.desc())

# todo
# @ns.route('/pending/committee')
# class EntityCode(Resource):
#     @api.marshal_with(entity_item)
#     @api.response(404, 'Changes not found.')
#     def get(self):
#         """ Returns changes by leading item, required code and year """
#         return Changes.query.filter(Changes.change_type_id == leading_item, Changes.req_code == req_code,
#                                     Changes.year == year).order_by(Changes.date.desc())
