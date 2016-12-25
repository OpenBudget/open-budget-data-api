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
