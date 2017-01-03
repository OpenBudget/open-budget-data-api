import logging

from flask_restplus import Resource

from open_budget_data_api.api.restplus import api
from open_budget_data_api.api.serializers import entity_item
from open_budget_data_api.models import Entities

log = logging.getLogger(__name__)

ns = api.namespace('entity', description='The Open Budget API : Entity')


@ns.route('/<id>')
class EntityCode(Resource):
    @api.marshal_with(entity_item)
    @api.response(404, 'Entity item not found.')
    def get(self, id):
        """ Returns entity by id """
        return Entities.query.filter(Entities.id == id).first()
