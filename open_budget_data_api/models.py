from sqlalchemy import Column, String, Integer, Float, Boolean, Date, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from .db import db


# generated with the assistance of sqlacodegen

class Budget(db.Model):
    __tablename__ = 'budget'
    code = Column(String, primary_key=True)
    year = Column(Integer, primary_key=True)
    title = Column(String)
    net_allocated = Column(Integer)
    net_revised = Column(Integer)
    net_used = Column(Float)
    gross_allocated = Column(Integer)
    gross_revised = Column(Integer)
    personnel_allocated = Column(Float)
    personnel_revised = Column(Float)
    commitment_allocated = Column(Integer)
    commitment_revised = Column(Integer)
    amounts_allocated = Column(Integer)
    amounts_revised = Column(Integer)
    contractors_allocated = Column(Float)
    contractors_revised = Column(Float)
    dedicated_allocated = Column(Integer)
    dedicated_revised = Column(Integer)
    equiv_code = Column(ARRAY(String))
    group_full = Column(ARRAY(String))
    group_top = Column(ARRAY(String))
    class_full = Column(ARRAY(String))
    class_top = Column(ARRAY(String))
    kind = Column(ARRAY(String))
    subkind = Column(ARRAY(String))
    active = Column(Boolean)

    changes = relationship("Changes",
                           primaryjoin="and_(Budget.code==Changes.budget_code, Budget.year==Changes.year)",
                           backref="budget")
    supports = relationship("Support",
                            primaryjoin="and_(Budget.code==Support.code, Budget.year==Support.year)",
                            backref="budget")
    exemptions = relationship("Exemption",
                              primaryjoin="Budget.code==Exemption.budget_code",
                              backref="budget")
    procurements = relationship("Procurement",
                                primaryjoin="Budget.code==Procurement.budget_code",
                                backref="budget")


# class BudgetApprovals(db.Model):
#     __tablename__ = 'budget_approvals'
#     year = Column(Integer, primary_key=True)
#     link = Column(String)
#     approval_date = Column(Date)
#     effect_date = Column(Date)
#     end_date = Column(Date)
#
#
# class ChangeExemption(db.Model):
#     __tablename__ = 'change_exemption'
#     publication_id = Column(String, primary_key=True)
#     time = Column(Date)
#     field = Column(String)
#     from_value = Column(String)
#     to_value = Column(String)
#     created = Column(Boolean)
#
#
# class ChangeHistory(db.Model):
#     __tablename__ = 'change_history'
#     model = Column(String, primary_key=True)
#     selector = Column(String)
#     time = Column(Date)
#     field = Column(String)
#     from_value = Column(String)
#     to_value = Column(String)
#     created = Column(Boolean)
#


class Changes(db.Model):
    __tablename__ = 'changes'
    year = Column(Integer, ForeignKey('budget.year'), primary_key=True)
    leading_item = Column(Integer)
    req_code = Column(Integer)
    req_title = Column(String)
    change_code = Column(Integer)
    change_title = Column(String)
    change_type_id = Column(Integer)
    change_type_name = Column(String)
    committee_id = Column(Integer)
    budget_code = Column(String, ForeignKey('budget.code'))
    budget_title = Column(String)
    net_expense_diff = Column(Integer)
    gross_expense_diff = Column(Integer)
    allocated_income_diff = Column(Integer)
    commitment_limit_diff = Column(Integer)
    personnel_max_diff = Column(Float)
    date = Column(String)
    pending = Column(Boolean)
    equiv_code = Column(ARRAY(String))


class Entity(db.Model):
    __tablename__ = 'entities'
    id = Column(String, primary_key=True)
    kind = Column(String)
    name = Column(String)
    flags = Column(String)
    manpower_contractor = Column(String)
    service_contractor = Column(String)
    gov_company = Column(Boolean)
    company_name = Column(String)
    company_status = Column(String)
    company_type = Column(String)
    company_government = Column(String)
    company_limit = Column(String)
    company_postal_code = Column(String)
    company_mafera = Column(String)
    company_address = Column(String)
    company_city = Column(String)
    lat = Column(Float)
    lng = Column(Float)

    supports = relationship("Support",
                            primaryjoin="Entity.id==Support.entity_id",
                            backref="entity")
    exemptions = relationship("Exemption",
                              primaryjoin="Entity.id==Exemption.entity_id",
                              backref="entity")
    procurements = relationship("Procurement",
                                primaryjoin="Entity.id==Procurement.entity_id",
                                backref="entity")


class Exemption(db.Model):
    __tablename__ = 'exemption'
    publication_id = Column(Integer, primary_key=True)
    budget_code = Column(String, ForeignKey('budget.code'))
    publisher = Column(String)
    regulation = Column(String)
    supplier = Column(String)
    supplier_id = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    claim_date = Column(Date)
    last_update_date = Column(Date)
    contact = Column(String)
    contact_email = Column(String)
    description = Column(String)
    volume = Column(Integer)
    reason = Column(String)
    decision = Column(String)
    url = Column(String)
    subjects = Column(ARRAY(String))
    source_currency = Column(String)
    page_title = Column(String)
    entity_id = Column(String, ForeignKey('entities.id'))
    entity_kind = Column(String)
    documents = Column(String)


class Procurement(db.Model):
    __tablename__ = 'procurement'
    publisher = Column(String, primary_key=True)
    purchasing_unit = Column(String)
    buyer_description = Column(String)
    budget_code = Column(String, ForeignKey('budget.code'))
    budget_title = Column(String)
    supplier_code = Column(String)
    supplier_name = Column(String)
    volume = Column(Float)
    executed = Column(Float)
    currency = Column(String)
    purchase_method = Column(String)
    manof_ref = Column(String)
    exemption_reason = Column(String)
    purpose = Column(String)
    order_id = Column(String)
    sensitive_order = Column(Boolean)
    report_date = Column(Date)
    report_title = Column(String)
    report_publisher = Column(String)
    report_subunit = Column(String)
    report_error = Column(String)
    report_href = Column(String)
    report_container_href = Column(String)
    report_year = Column(Integer)
    report_period = Column(Integer)
    order_date = Column(Date)
    entity_id = Column(String, ForeignKey('entities.id'))
    entity_kind = Column(String)


class Support(db.Model):
    __tablename__ = 'supports'
    year = Column(Integer, ForeignKey('budget.year'), primary_key=True)
    subject = Column(String)
    code = Column(String, ForeignKey('budget.code'))
    recipient = Column(String)
    kind = Column(String)
    title = Column(String)
    num_used = Column(Integer)
    amount_allocated = Column(Integer)
    amount_supported = Column(Integer)
    entity_id = Column(String, ForeignKey('entities.id'))
    entity_kind = Column(String)

# class Tender(db.Model):
#     __tablename__ = 'tender'
#     publication_id = Column(Integer, primary_key=True)
#     publisher = Column(String)
#     publish_date = Column(Date)
#     claim_date = Column(Date)
#     claim_time = Column(String)
#     last_update_date = Column(Date)
#     description = Column(String)
#     url = Column(String)
#     subjects = Column(String)
#     status = Column(String)
