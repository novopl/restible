# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# 3rd party imports
import pytest

# local imports
from restible import RestEndpoint


def test_works_for_query(rf):
    request = rf.get('/test')

    args = RestEndpoint.build_handler_args('query', request)

    assert 'pk' not in args
    assert 'filters' in args


def test_extracts_filters_from_get_params_for_query(rf):
    request = rf.get('/test', data={
        'filter1': 'value1',
        'filter2': 123,
        'filter3': 3.14159
    })

    args = RestEndpoint.build_handler_args('query', request)

    assert 'pk' not in args
    assert 'filters' in args

    filters = args['filters']
    assert len(filters) == 3
    assert 'filter1' in filters
    assert 'filter2' in filters
    assert 'filter3' in filters
    assert filters['filter1'] == 'value1'
    assert filters['filter2'] == 123
    assert filters['filter3'] == 3.14159


def test_works_for_get(rf):
    request = rf.get('/test')

    args = RestEndpoint.build_handler_args('get', request)

    assert args == {}


def test_works_for_create(rf):
    request = rf.post('/test', data={}, content_type='application/json')

    args = RestEndpoint.build_handler_args('create', request)

    assert 'pk' not in args
    assert 'data' in args
    assert args['data'] == {}


def test_works_for_update(rf):
    request = rf.post('/test', data={}, content_type='application/json')

    args = RestEndpoint.build_handler_args('update', request)

    assert 'data' in args
    assert args['data'] == {}


def test_raises_ValueError_on_invalid_json(rf):
    request = rf.post('/test', data='asasdfasdf',
                      content_type='application/json')

    with pytest.raises(ValueError):
        RestEndpoint.build_handler_args('update', request)
