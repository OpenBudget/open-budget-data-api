import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from sqlalchemy.sql import and_

from open_budget_data_api.models import Budget as BudgetModel, Changes as ChangeModel, Entity as EntityModel, \
    Exemption as ExemptionModel, Procurement as ProcurementModel, Support as SupportModel


class Budget(SQLAlchemyObjectType):
    class Meta:
        model = BudgetModel
        interfaces = (relay.Node,)


class Change(SQLAlchemyObjectType):
    class Meta:
        model = ChangeModel
        interfaces = (relay.Node,)


class Entity(SQLAlchemyObjectType):
    class Meta:
        model = EntityModel
        interfaces = (relay.Node,)


class Exemption(SQLAlchemyObjectType):
    class Meta:
        model = ExemptionModel
        interfaces = (relay.Node,)


class Procurement(SQLAlchemyObjectType):
    class Meta:
        model = ProcurementModel
        interfaces = (relay.Node,)


class Support(SQLAlchemyObjectType):
    class Meta:
        model = SupportModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    budget = SQLAlchemyConnectionField(Budget, description="Budget by code and year",
                                       code=graphene.String(), year=graphene.Int(), where=graphene.String(),
                                       orderBy=graphene.String(), page=graphene.Int(), perPage=graphene.Int())

    change = SQLAlchemyConnectionField(Change, description="Change by code and year",
                                       code=graphene.String(), year=graphene.Int(), where=graphene.String(),
                                       orderBy=graphene.String(), page=graphene.Int(), perPage=graphene.Int())

    entity = SQLAlchemyConnectionField(Entity, description="Entity by id",
                                       id=graphene.Int(), where=graphene.String(), orderBy=graphene.String(),
                                       page=graphene.Int(), perPage=graphene.Int())

    exemption = SQLAlchemyConnectionField(Exemption, description="Exemption",
                                          where=graphene.String(), orderBy=graphene.String(),
                                          page=graphene.Int(), perPage=graphene.Int())

    procurement = SQLAlchemyConnectionField(Procurement, description="Procurement",
                                            where=graphene.String(), orderBy=graphene.String(),
                                            page=graphene.Int(), perPage=graphene.Int())

    support = SQLAlchemyConnectionField(Support, description="Support",
                                        where=graphene.String(), orderBy=graphene.String(),
                                        page=graphene.Int(), perPage=graphene.Int())

    def resolve_budget(self, args, foo, bar):
        year = args.get('year')
        code = args.get('code')
        query = BudgetModel.query
        if code is not None:
            query = query.filter(BudgetModel.code == code)
        if year is not None:
            query = query.filter(BudgetModel.year == year)
        query = where_order_by(args, query)
        return query.all()

    def resolve_change(self, args, foo, bar):
        year = args.get('year')
        code = args.get('code')
        query = ChangeModel.query
        if code is not None:
            query = query.filter(ChangeModel.budget_code == code)
        if year is not None:
            query = query.filter(ChangeModel.year == year)
        query = where_order_by(args, query)
        return query.all()

    def resolve_entity(self, args, foo, bar):
        id = args.get('id')
        query = EntityModel.query
        if id is not None:
            query = query.filter(EntityModel.id == id)
        query = where_order_by(args, query)
        return query.all()

    def resolve_exemption(self, args, foo, bar):
        query = ExemptionModel.query
        query = where_order_by(args, query)
        return query.all()

    def resolve_procurement(self, args, foo, bar):
        query = ProcurementModel.query
        query = where_order_by(args, query)
        return query.all()

    def resolve_support(self, args, foo, bar):
        query = SupportModel.query
        query = where_order_by(args, query)
        return query.all()


def where_order_by(args, query):
    where = args.get('where')
    orderBy = args.get('orderBy')
    page = args.get('page', 1)
    per_page = args.get('perPage', 10)
    if where is not None:
        query = query.filter(and_(where))
    if orderBy is not None:
        query = query.order_by(orderBy)
    return query.limit(per_page).offset((page - 1) * per_page)


scheme = graphene.Schema(query=Query, types=[Budget, Entity, Exemption, Procurement, Support])
