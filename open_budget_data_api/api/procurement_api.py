import logging

from flask_restplus import Resource

from open_budget_data_api.api.restplus import api, paginate, page_args, page_of
from open_budget_data_api.api.serializers import procurement_item
from open_budget_data_api.models import Procurement

log = logging.getLogger(__name__)

ns = api.namespace('procurement', description='The Open Budget API : Procurement')


@ns.route('/<code>')
@api.expect(page_args, validate=False)
class ProcurementBudget(Resource):
    @api.marshal_with(page_of(procurement_item))
    @api.response(404, 'Procurement item not found.')
    def get(self, code):
        """ Returns procurements for code. """
        return paginate(page_args, Procurement.query.filter(Procurement.budget_code == code))


@ns.route('/entity/<entity_id>')
@api.expect(page_args, validate=False)
class ProcurementEntity(Resource):
    @api.marshal_with(page_of(procurement_item))
    @api.response(404, 'Procurement item not found.')
    def get(self, entity_id):
        """ Returns procurements for entity. """
        return paginate(page_args, Procurement.query.filter(Procurement.entity_id == entity_id))
