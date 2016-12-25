from flask_restplus import fields

from open_budget_data_api.api.restplus import api

budget_item = api.model('Budget Item', {
    'code': fields.String(description='The budget item code'),
    'year': fields.Integer(description='The budget item year'),
    'title': fields.String(description='Title'),
    'net_allocated': fields.Integer,
    'net_revised': fields.Integer,
    'net_used': fields.Integer,
    'gross_allocated': fields.Integer,
    'gross_revised': fields.Integer,
    'personnel_allocated': fields.Float,
    'personnel_revised': fields.Float,
    'commitment_allocated': fields.Integer,
    'commitment_revised': fields.Integer,
    'amounts_allocated': fields.Integer,
    'amounts_revised': fields.Integer,
    'contractors_allocated': fields.Integer,
    'contractors_revised': fields.Integer,
    'dedicated_allocated': fields.Integer,
    'dedicated_revised': fields.Integer,
    # 'equiv_code': fields.List(fields.String),
    # 'group_full': fields.List(fields.String),
    # 'group_top': fields.List(fields.String),
    # 'class_full': fields.List(fields.String),
    # 'class_top': fields.List(fields.String),
    # 'kind': fields.List(fields.String),
    # 'subkind': fields.List(fields.String),
})
