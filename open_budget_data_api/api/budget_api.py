import logging

from flask_restplus import Resource
from sqlalchemy.sql.expression import func

from open_budget_data_api.api.restplus import api, paginate, page_args, page_of
from open_budget_data_api.api.serializers import budget_item
from open_budget_data_api.models import Budget

log = logging.getLogger(__name__)

ns = api.namespace('budget', description='The Open Budget API : Budget')


def code_prefix(code, depth):
    return Budget.code.like(code + '%') & func.length(Budget.code) == depth


@ns.route('/<code>')
@api.expect(page_args, validate=False)
class BudgetCode(Resource):
    @api.marshal_with(page_of(budget_item))
    @api.response(404, 'Budget item not found.')
    def get(self, code):
        """ Returns a budget by code. """
        return paginate(page_args, Budget.query.filter(Budget.code == code).order_by(Budget.year.desc()))


@ns.route('/<code>/<int:year>')
class BudgetCodeYear(Resource):
    @api.marshal_with(budget_item)
    @api.response(404, 'Budget item not found.')
    def get(self, code, year):
        """ Returns a budget by code and year. """
        return Budget.query.filter(Budget.code == code, Budget.year == year).first()


@ns.route('/<code>/<int:year>/kids')
@api.expect(page_args, validate=False)
class BudgetKids(Resource):
    @api.marshal_with(page_of(budget_item))
    @api.response(404, 'Budget item not found.')
    def get(self, code, year):
        """ Returns budget by code prefix and year. """
        return paginate(page_args, Budget.query.filter(code_prefix(code, len(code) / 2) & Budget.year == year))


@ns.route('/<code>/<int:year>/active-kids')
@api.expect(page_args, validate=False)
class BudgetActiveKids(Resource):
    @api.marshal_with(page_of(budget_item))
    @api.response(404, 'Budget item not found.')
    def get(self, code, year):
        """ Returns active budget by code prefix and year. """
        return paginate(page_args, Budget.query.filter(
            code_prefix(code, len(code) / 2) & Budget.year == year & Budget.active == True))


@ns.route('/<code>/<int:year>/parents')
@api.expect(page_args, validate=False)
class BudgetParents(Resource):
    @api.marshal_with(page_of(budget_item))
    @api.response(404, 'Budget item not found.')
    def get(self, code, year):
        """ Returns budget by code parents and year. """
        codes = [code[:l] for l in range(2, len(code) + 1, 2)]
        print('codes: ' + codes)
        return paginate(page_args, Budget.query.filter(Budget.code.in_(codes) & Budget.year == year))


@ns.route('/<code>/<int:year>/depth/<int:depth>')
@api.expect(page_args, validate=False)
class BudgetCodeDepth(Resource):
    @api.marshal_with(page_of(budget_item))
    @api.response(404, 'Budget item not found.')
    def get(self, code, year, depth):
        """ Returns a budget by code depth and year. """
        return paginate(page_args, Budget.query.filter(code_prefix(code, depth) & Budget.year == year))


@ns.route('/<code>/<int:year>/equiv')
class BudgetEquiv(Resource):
    @api.marshal_with(page_of(budget_item))
    @api.response(404, 'Budget item not found.')
    def get(self, code, year):
        """ Returns a budget by equiv code and year, grouped by year and ordered by code. """
        equiv_codes = [('%s/%s' % (year, code))]
        query = Budget.query.filter(Budget.code == code & Budget.year == year | Budget.equiv_code.contains(equiv_codes))
        return query.group_by(Budget.year).order_by(Budget.code)


@ns.route('/<code>/<int:year>/matches')
class BudgetEquiv(Resource):
    @api.marshal_with(page_of(budget_item))
    @api.response(404, 'Budget item not found.')
    def get(self, code, year):
        """ Returns a budget by equiv code and year, grouped by year and ordered by code. """
        equiv_code = '%s/%s' % (year, code)
        return paginate(page_args, Budget.query.filter(
            code_prefix(code, len(code) / 2) & Budget.year == year & Budget.match_status.not_empty == True))
