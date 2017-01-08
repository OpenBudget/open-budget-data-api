import datetime
import logging

from flask_restplus import Resource

from open_budget_data_api.api.restplus import api, paginate, page_of, page_args
from open_budget_data_api.api.serializers import exemption_item
from open_budget_data_api.models import Exemption

log = logging.getLogger(__name__)

ns = api.namespace('exemption', description='The Open Budget API : Exemption')


@ns.route('/publication/<int:publication_id>')
@api.expect(page_args, validate=False)
class ExemptionPublication(Resource):
    @api.marshal_with(exemption_item)
    @api.response(404, 'Exemption item not found.')
    def get(self, publication_id):
        """ Returns exemption for publication id. """
        return Exemption.query.filter(Exemption.publication_id == publication_id).first()


@ns.route('/entity/<entity_id>')
@api.expect(page_args, validate=False)
class ExemptionEntity(Resource):
    @api.marshal_with(exemption_item)
    @api.response(404, 'Exemption item not found.')
    def get(self, entity_id):
        """ Returns exemption for entity id. """
        return Exemption.query.filter(Exemption.entity_id == entity_id).first()


@ns.route('/budget/<code>')
@api.expect(page_args, validate=False)
class ExemptionBudget(Resource):
    @api.marshal_with(page_of(exemption_item))
    @api.response(404, 'Exemption item not found.')
    def get(self, code):
        """ Returns exemptions for budget code. """
        return paginate(page_args, Exemption.query.filter(Exemption.budget_code == code))


@ns.route('/updated/<from_date>/<to_date>')
@api.expect(page_args, validate=False)
class ExemptionUpdated(Resource):
    @api.marshal_with(page_of(exemption_item))
    @api.response(404, 'Exemption item not found.')
    def get(self, from_date, to_date):
        """ Returns exemptions updated between 'from' and 'to'. """
        return paginate(page_args, Exemption.query.filter(
            Exemption.last_update_date >= from_date & Exemption.last_update_date <= to_date))


@ns.route('/new')
@api.expect(page_args, validate=False)
class ExemptionNew(Resource):
    @api.marshal_with(page_of(exemption_item))
    @api.response(404, 'Exemption item not found.')
    def get(self):
        """ Returns exemption last updated. """
        return paginate(page_args, Exemption.query.order_by(Exemption.last_update_date.desc))


@ns.route('/new/<int:days>')
@api.expect(page_args, validate=False)
class ExemptionNewBy(Resource):
    @api.marshal_with(page_of(exemption_item))
    @api.response(404, 'Exemption item not found.')
    def get(self, days):
        """ Returns exemptions since the last given 'days'. """
        first_date = datetime.datetime.now() - datetime.timedelta(days=days + 1)
        return paginate(page_args, Exemption.query.filter(
            Exemption.last_update_date >= first_date).order_by(Exemption.last_update_date.desc))
