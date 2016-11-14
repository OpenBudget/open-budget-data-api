from flask_restful import Resource
from peewee import R, fn, IntegerField, FloatField, CharField

from .models import Budget


class ObudgetResource(Resource):
    MODEL = None

    def get(self, **kwargs):
        q = self.MODEL.select()
        q = q.where(*self.where(**kwargs))
        q = q.dicts()
        return list(q)

    def where(self, **kwargs):
        raise NotImplementedError()


class BudgetHandler(ObudgetResource):
    MODEL = Budget
    PATHS = [
        'budget/<code>',
        'budget/<code>/<int:year>',
        'budget/<code>/<int:year>/<kind>/',
        'budget/<code>/<int:year>/<kind>/<int:depth>',
    ]

    def __init__(self, **kwargs):
        super(BudgetHandler, self).__init__(**kwargs)
        self.measures = []
        self.identifiers = []
        for _field in getattr(self.MODEL, '_meta').fields.keys():
            field = getattr(self.MODEL, _field)
            if isinstance(field, IntegerField) or \
               isinstance(field, FloatField):
                if field != self.MODEL.year:
                    self.measures.append(field)
            elif isinstance(field, CharField):
                self.identifiers.append(field)

    def get(self, **kwargs):
        if kwargs.get('kind') == 'equivs':
            ret = list(self.get_equivs(**kwargs).dicts())
            print(ret)
            return ret
        else:
            return super(BudgetHandler, self).get(**kwargs)

    def get_equivs(self, year=None, code=None, kind=None):
        equiv_code = '%s/%s' % (year, code)
        single = self.MODEL.get(self.MODEL.code == code,
                                self.MODEL.year == year)
        print("MMM", self.measures)
        q = self.MODEL.select(R('%s', single.code).alias('code'),
                              R('%s', single.title).alias('title'),
                              self.MODEL.year,
                              *self.identifiers,
                              *(fn.sum(m).cast('int').alias(m.name) for m in self.measures),
                              fn.Array_Agg(self.MODEL.code).alias('orig_codes')
                              )
        q = q.where(((self.MODEL.year == year) & (self.MODEL.code == code)) |
                    (R('equiv_code @> ARRAY[%s]', equiv_code))
                    )
        q = q.group_by(self.MODEL.year,
                       *self.identifiers,)
        q = q.order_by(self.MODEL.year.asc())
        return q

    def where(self, code=None, year=None, kind=None, depth=None, **kwargs):
        ret = []
        if year is not None:
            ret.append(self.MODEL.year == int(year))
        if kind is None:
            ret.append(self.MODEL.code == code)
        elif kind == 'kids':
            ret.append(self.MODEL.code.startswith(code))
            ret.append(R('length(code)=%s', len(code)+2))
        elif kind == 'active-kids':
            ret.append(self.MODEL.code.startswith(code))
            ret.append(self.MODEL.active == True)
            ret.append(R('length(code)=%s', len(code)+2))
        elif kind == "depth" and depth is not None:
            depth = int(depth)
            ret.append(self.MODEL.code.startswith(code))
            ret.append(R('length(code)=%s', (depth+1)*2))
        elif kind == 'parents':
            codes = [code[:l] for l in range(2,len(code)+1,2) ]
            ret.append(self.MODEL.code << codes)
        else:
            raise NotImplementedError()

        #
        #
        #
        #     _lines = BudgetLine.query(
        #             ndb.OR(
        #                     ndb.AND(BudgetLine.year==year,
        #                             BudgetLine.code==code),
        #                     BudgetLine.equiv_code==equiv_code)
        #             ).order(BudgetLine.year).fetch(batch_size=50)
        #     lines = []
        #     by_year = itertools.groupby(_lines, lambda x:x.year)
        #     for _year, yearly in by_year:
        #         rec = { 'year': _year,
        #                 'code': code,
        #                 'title': _lines[-1].title,
        #                 'orig_codes':[] }
        #         base = dict((k,None) for k in aggregated_budget_fields)
        #         for item in yearly:
        #             for k,v in item.to_dict().iteritems():
        #                 if k in aggregated_budget_fields and v is not None:
        #                     rec.setdefault(k,0)
        #                     rec[k] += v
        #             rec['orig_codes'].append(item.code)
        #         base.update(rec)
        #         lines.append(base)
        # elif kind == "matches":
        #     lines = BudgetLine.query(code_starts_with(BudgetLine,code),BudgetLine.year==year,BudgetLine.match_status.not_empty==True)
        #

        return ret
