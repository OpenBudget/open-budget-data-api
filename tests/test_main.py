# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import json

import pytest

BUDGET_ITEM_POLICY = {
    "/keys": {
        "allowed_missing_items": ["match_status", "active", "prefixes",
                                  "explanation", "analysis_short_term_yearly_change",
                                  "depth", "gross_used"]
    },
    ".contractors_revised": {
        "type_match": False
    },
    ".contractors_allocated": {
        "type_match": False
    },
    ".net_used": {
        "type_match": False
    },
    ".class_top": {
        "compare_as_sets": True
    },
    ".class_full": {
        "compare_as_sets": True
    },
    ".group_top": {
        "compare_as_sets": True
    },
    ".group_full": {
        "compare_as_sets": True
    },
    ".kind": {
        "compare_as_sets": True
    },
    ".orig_codes": {
        "compare_as_sets": True
    }
}

POLICIES = {
    'budget_item': BUDGET_ITEM_POLICY,
    'budget_items': dict(('[]'+k, v) for k,v in BUDGET_ITEM_POLICY.items())
}


def compare_objects(contexts, ctx_key, a, b):
    context = contexts.get(ctx_key, {})
    if type(a) is not type(b):
        if None not in [a, b] or any([a, b]):
            # Allow matching None's and False-y values
            if context.get('type_match', True):
                raise ValueError('{}: Mismatching types ({!s} != {!s})'.format(ctx_key, type(a), type(b)))
        return True

    if type(a) is list:
        if len(a) != len(b):
            if context.get('length_match', True):
                raise ValueError('{}: Mismatching lengths ({} != {})'.format(ctx_key, len(a), len(b)))
        if context.get('compare_as_sets', False):
            return compare_objects(contexts, ctx_key, set(a), set(b))
        elif context.get('list_traversal', True):
            return all(compare_objects(contexts, ctx_key+'[]', _a, _b)
                       for _a, _b in zip(a, b))

    elif type(a) is set:
        allowed_extra_items = set(context.get('allowed_extra_items', []))
        allowed_missing_items = set(context.get('allowed_missing_items', []))
        if len(a-b-allowed_missing_items) != 0:
            raise ValueError('{}: Missing items on 2nd set {}'.format(ctx_key, a-b-allowed_missing_items))
        if len(b-a-allowed_extra_items) != 0:
            raise ValueError('{}: Missing items on 1st set {}'.format(ctx_key, b-a-allowed_extra_items))

    elif type(a) is dict:
        keys_a, keys_b = set(a.keys()), set(b.keys())
        compare_objects(contexts, ctx_key+'/keys', keys_a, keys_b)
        for key in keys_a & keys_b:
            compare_objects(contexts, ctx_key+'.'+key, a[key], b[key])

    elif type(a) is float:
        if abs(a - b) > 1:
            if context.get('values_match', True):
                raise ValueError('{}: Mismatching values ({!r} !=~ {!r})'.format(ctx_key, a, b))

    else:
        if a != b:
            if context.get('values_match', True):
                raise ValueError('{}: Mismatching values ({!r} != {!r})'.format(ctx_key, a, b))

    return True


@pytest.fixture
def flask_app():
    from open_budget_data_api.main import app
    return app.test_client()


def _test_single_prerecorded_api_call(app, path, prerecorded, contexts={}):
    """Test a single request and compare it to the expected output"""
    rv = app.get(path)
    assert rv.status_code == 200
    response = json.loads(rv.get_data().decode('utf8'))
    if type(prerecorded) is list:
        response = response['items']
    compare_objects(contexts, '', prerecorded, response)
    return False


prerecorded_responses = \
    os.walk(
        os.path.join(
            os.path.dirname(__file__),
            'api_fixtures'
        )
    )
for dirpath, _, filenames in prerecorded_responses:
    for filename in filenames:
        parts = open(os.path.join(dirpath, filename), encoding='utf8').read().split('\n\n')
        if len(parts) == 2:
            _path, _response = parts
            _policy = None
        else:
            _path, _response, _policy = parts
            _policy = _policy.strip()
        _response = json.loads(_response)
        _policies = POLICIES.get(_policy, {})

        def inner(__path, __response, __policies):
            def inner2(flask_app):
                return _test_single_prerecorded_api_call(flask_app, __path, __response, __policies)
            return inner2
        globals()['test_prerecorded_%s' % filename] = inner(_path, _response, _policies)
