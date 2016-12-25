from sqlalchemy.types import ARRAY

from db import db


# generated with the assistance of sqlacodegen

class Budget(db.Model):
    __tablename__ = 'budget'
    code = db.Column(db.String, primary_key=True)
    year = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    net_allocated = db.Column(db.Integer)
    net_revised = db.Column(db.Integer)
    net_used = db.Column(db.Integer)
    gross_allocated = db.Column(db.Integer)
    gross_revised = db.Column(db.Integer)
    personnel_allocated = db.Column(db.Float)
    personnel_revised = db.Column(db.Float)
    commitment_allocated = db.Column(db.Integer)
    commitment_revised = db.Column(db.Integer)
    amounts_allocated = db.Column(db.Integer)
    amounts_revised = db.Column(db.Integer)
    contractors_allocated = db.Column(db.Integer)
    contractors_revised = db.Column(db.Integer)
    dedicated_allocated = db.Column(db.Integer)
    dedicated_revised = db.Column(db.Integer)
    # equiv_code = ARRAY(db.String)
    # group_full = ARRAY(db.String)
    # group_top = ARRAY(db.String)
    # class_full = ARRAY(db.String)
    # class_top = ARRAY(db.String)
    # kind = ARRAY(db.String)
    # subkind = ARRAY(db.String)


# class BudgetApprovals(db.Model):
#     __tablename__ = 'budget_approvals'
#     year = db.Column(db.Integer, primary_key=True)
#     link = db.Column(db.String)
#     approval_date = db.Column(db.Date)
#     effect_date = db.Column(db.Date)
#     end_date = db.Column(db.Date)
#
#
# class ChangeExemption(db.Model):
#     __tablename__ = 'change_exemption'
#     publication_id = db.Column(db.String, primary_key=True)
#     time = db.Column(db.Date)
#     field = db.Column(db.String)
#     from_value = db.Column(db.String)
#     to_value = db.Column(db.String)
#     created = db.Column(db.Boolean)
#
#
# class ChangeHistory(db.Model):
#     __tablename__ = 'change_history'
#     model = db.Column(db.String, primary_key=True)
#     selector = db.Column(db.String)
#     time = db.Column(db.Date)
#     field = db.Column(db.String)
#     from_value = db.Column(db.String)
#     to_value = db.Column(db.String)
#     created = db.Column(db.Boolean)
#
#
# class Changes(db.Model):
#     __tablename__ = 'changes'
#     year = db.Column(db.Integer, primary_key=True)
#     leading_item = db.Column(db.Integer)
#     req_code = db.Column(db.Integer)
#     req_title = db.Column(db.String)
#     change_code = db.Column(db.Integer)
#     change_title = db.Column(db.String)
#     change_type_id = db.Column(db.Integer)
#     change_type_name = db.Column(db.String)
#     committee_id = db.Column(db.Integer)
#     budget_code = db.Column(db.String)
#     budget_title = db.Column(db.String)
#     net_expense_diff = db.Column(db.Integer)
#     gross_expense_diff = db.Column(db.Integer)
#     allocated_income_diff = db.Column(db.Integer)
#     commitment_limit_diff = db.Column(db.Integer)
#     personnel_max_diff = db.Column(db.Float)
#     date = db.Column(db.String)
#     pending = db.Column(db.Boolean)
#     equiv_code = ARRAY(db.String)
#

class Entities(db.Model):
    __tablename__ = 'entities'
    id = db.Column(db.String, primary_key=True)
    kind = db.Column(db.String)
    name = db.Column(db.String)
    flags = db.Column(db.String)
    manpower_contractor = db.Column(db.String)
    service_contractor = db.Column(db.String)
    gov_company = db.Column(db.Boolean)
    company_name = db.Column(db.String)
    company_status = db.Column(db.String)
    company_type = db.Column(db.String)
    company_government = db.Column(db.String)
    company_limit = db.Column(db.String)
    company_postal_code = db.Column(db.String)
    company_mafera = db.Column(db.String)
    company_address = db.Column(db.String)
    company_city = db.Column(db.String)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)


class Exemption(db.Model):
    __tablename__ = 'exemption'
    publication_id = db.Column(db.Integer, primary_key=True)
    budget_code = db.Column(db.String)
    publisher = db.Column(db.String)
    regulation = db.Column(db.String)
    supplier = db.Column(db.String)
    supplier_id = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    claim_date = db.Column(db.Date)
    last_update_date = db.Column(db.Date)
    contact = db.Column(db.String)
    contact_email = db.Column(db.String)
    description = db.Column(db.String)
    volume = db.Column(db.Integer)
    reason = db.Column(db.String)
    decision = db.Column(db.String)
    url = db.Column(db.String)
    subjects = ARRAY(db.String)
    source_currency = db.Column(db.String)
    page_title = db.Column(db.String)
    entity_id = db.Column(db.String)
    entity_kind = db.Column(db.String)
    documents = db.Column(db.String)


class Procurement(db.Model):
    __tablename__ = 'procurement'
    publisher = db.Column(db.String, primary_key=True)
    purchasing_unit = db.Column(db.String)
    buyer_description = db.Column(db.String)
    budget_code = db.Column(db.String)
    budget_title = db.Column(db.String)
    supplier_code = db.Column(db.String)
    supplier_name = db.Column(db.String)
    volume = db.Column(db.Float)
    executed = db.Column(db.Float)
    currency = db.Column(db.String)
    purchase_method = db.Column(db.String)
    manof_ref = db.Column(db.String)
    exemption_reason = db.Column(db.String)
    purpose = db.Column(db.String)
    order_id = db.Column(db.String)
    sensitive_order = db.Column(db.Boolean)
    report_date = db.Column(db.Date)
    report_title = db.Column(db.String)
    report_publisher = db.Column(db.String)
    report_subunit = db.Column(db.String)
    report_error = db.Column(db.String)
    report_href = db.Column(db.String)
    report_container_href = db.Column(db.String)
    report_year = db.Column(db.Integer)
    report_period = db.Column(db.Integer)
    order_date = db.Column(db.Date)
    entity_id = db.Column(db.String)
    entity_kind = db.Column(db.String)


class Support(db.Model):
    __tablename__ = 'supports'
    year = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String)
    code = db.Column(db.String)
    recipient = db.Column(db.String)
    kind = db.Column(db.String)
    title = db.Column(db.String)
    num_used = db.Column(db.Integer)
    amount_allocated = db.Column(db.Integer)
    amount_supported = db.Column(db.Integer)
    entity_id = db.Column(db.String)
    entity_kind = db.Column(db.String)

# class Tender(db.Model):
#     __tablename__ = 'tender'
#     publication_id = db.Column(db.Integer, primary_key=True)
#     publisher = db.Column(db.String)
#     publish_date = db.Column(db.Date)
#     claim_date = db.Column(db.Date)
#     claim_time = db.Column(db.String)
#     last_update_date = db.Column(db.Date)
#     description = db.Column(db.String)
#     url = db.Column(db.String)
#     subjects = db.Column(db.String)
#     status = db.Column(db.String)
