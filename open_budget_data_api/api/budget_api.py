import logging

from flask_restplus import Resource
from sqlalchemy import func, sql

from .restplus import api, paginate, page_args, page_of
from .serializers import budget_item, equiv_budget_item
from ..models import Budget

log = logging.getLogger(__name__)

ns = api.namespace('budget', description='The Open Budget API : Budget')


BudgetMeasures = [getattr(Budget, k)
                  for k, v in Budget.__table__.columns._data.items()
                  if k not in {'year'} and v.type.python_type in (int, float)]
BudgetIdentifiers = [getattr(Budget, k)
                     for k, v in Budget.__table__.columns._data.items()
                     if k not in {'code', 'title'} and v.type.python_type in (str, )]


@ns.route('/<code>')
@api.expect(page_args, validate=False)
class BudgetCode(Resource):
    @api.marshal_with(page_of(budget_item))
    @api.response(404, 'Budget item not found.')
    def get(self, code):
        """ Returns a budget by code. """
        return paginate(page_args,
                        Budget.query
                              .filter(Budget.code == code)
                              .order_by(Budget.year.asc())
                        )


@ns.route('/<code>/<int:year>')
class BudgetCodeYear(Resource):
    @api.marshal_with(budget_item)
    @api.response(404, 'Budget item not found.')
    def get(self, code, year):
        """ Returns a budget by code and year. """
        return Budget.query\
                     .filter(Budget.code == code,
                             Budget.year == year).first()


@ns.route('/<code>/<int:year>/kids')
@api.expect(page_args, validate=False)
class BudgetKids(Resource):
    @api.marshal_with(page_of(budget_item))
    @api.response(404, 'Budget item not found.')
    def get(self, code, year):
        """ Returns all budget kids by code prefix and year. """
        return paginate(page_args,
                        Budget.query
                              .filter(Budget.code.like(code + '%'),
                                      func.length(Budget.code) == len(code) + 2,
                                      Budget.year == year)
                              .order_by(Budget.code.asc())
                        )


@ns.route('/<code>/<int:year>/active-kids')
@api.expect(page_args, validate=False)
class BudgetActiveKids(Resource):
    @api.marshal_with(page_of(budget_item))
    @api.response(404, 'Budget item not found.')
    def get(self, code, year):
        """ Returns active budget kids by code prefix and year. """
        return paginate(page_args,
                        Budget.query
                              .filter(Budget.code.like(code + '%'),
                                      func.length(Budget.code) == len(code) + 2,
                                      Budget.year == year,
                                      Budget.active == True) # noqa
                              .order_by(Budget.code.asc())
                        )


@ns.route('/<code>/<int:year>/parents')
@api.expect(page_args, validate=False)
class BudgetParents(Resource):
    @api.marshal_with(page_of(budget_item))
    @api.response(404, 'Budget item not found.')
    def get(self, code, year):
        """ Returns budget by code parents and year. """
        codes = [code[:l] for l in range(2, len(code) + 1, 2)]
        return paginate(page_args,
                        Budget.query
                              .filter(Budget.code.in_(codes),
                                      Budget.year == year)
                        )


@ns.route('/<code>/<int:year>/depth/<int:depth>')
@api.expect(page_args, validate=False)
class BudgetCodeDepth(Resource):
    @api.marshal_with(page_of(budget_item))
    @api.response(404, 'Budget item not found.')
    def get(self, code, year, depth):
        """ Returns a budget by code depth and year. """
        return paginate(page_args,
                        Budget.query
                              .filter(Budget.code.like(code + '%'),
                                      func.length(Budget.code) == (depth+1)*2,
                                      Budget.year == year)
                              .order_by(Budget.code.asc())
                        )


@ns.route('/<code>/<int:year>/equivs')
class BudgetEquiv(Resource):
    @api.marshal_with(page_of(equiv_budget_item))
    @api.response(404, 'Budget item not found.')
    def get(self, code, year):
        """ Returns a budget by equiv code and year, grouped by year and ordered by code. """
        # equiv_codes = [('%s/%s' % (year, code))]
        # query = Budget.query.filter(Budget.code == code,
        #                             Budget.year == year | Budget.equiv_code.contains(equiv_codes))
        # return query.group_by(Budget.year).order_by(Budget.code)

        equiv_code = '%s/%s' % (year, code)
        single = Budget.query.filter(Budget.code == code, Budget.year == year).first()
        query = Budget.query\
                      .with_entities(
                                 sql.expression.bindparam("code", single.code),
                                 sql.expression.bindparam("title", single.title),
                                 Budget.year,
                                 *BudgetIdentifiers,
                                 *(func.Sum(m).label(m.name) for m in BudgetMeasures),
                                 func.array_agg(Budget.code).label('orig_codes')
                                )\
                      .filter(((Budget.year == year) & (Budget.code == code)) |
                              Budget.equiv_code.any(equiv_code))\
                      .group_by(Budget.year, *BudgetIdentifiers)\
                      .order_by(Budget.year.asc())
        return paginate(page_args,
                        query)


@ns.route('/<code>/<int:year>/matches')
class BudgetMatches(Resource):
    @api.marshal_with(page_of(budget_item))
    @api.response(404, 'Budget item not found.')
    def get(self, code, year):
        """ Returns a budget by equiv code and year, grouped by year and ordered by code. """
        return paginate(page_args,
                        Budget.query.filter(Budget.code.like(code + '%'),
                                            func.length(Budget.code) == len(code) + 2,
                                            Budget.year == year,
                                            Budget.match_status.not_empty is True))
