from playhouse.postgres_ext import Model, CharField, IntegerField, CompositeKey, FloatField, BooleanField, ArrayField, JSONField
from .config import database


class Budget(Model):
    year = IntegerField()
    code = CharField()

    title = CharField()

    net_allocated = IntegerField()
    gross_allocated = IntegerField()

    dedicated_allocated = IntegerField()
    commitment_allocated = IntegerField()
    personnel_allocated = FloatField()
    contractors_allocated = FloatField()
    amounts_allocated = IntegerField()

    net_revised = IntegerField()
    gross_revised = IntegerField()

    dedicated_revised = IntegerField()
    commitment_revised = IntegerField()
    personnel_revised = FloatField()
    contractors_revised = FloatField()
    amounts_revised = IntegerField()

    net_used = FloatField()

    group_top = ArrayField(CharField)
    group_full = ArrayField(CharField)

    class_top = ArrayField(CharField)
    class_full = ArrayField(CharField)

    kind = ArrayField(CharField)
    subkind = ArrayField(CharField)

    equiv_code = ArrayField(CharField)

    # explanation = CharField()

    # active = BooleanField()

    # match_status = JSONField()

    # analysis_short_term_yearly_change = IntegerField()
    
    class Meta:
        database = database
        primary_key = CompositeKey('year', 'code')
