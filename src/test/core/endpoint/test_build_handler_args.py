# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# local imports
from restible import RestEndpoint


#####################
#     Test data     #
#####################


class FakeRequest(object):
    def __init__(self, **kwargs):
        self.body = kwargs.pop('body', '').encode('utf-8')
        self.GET = kwargs.pop('query', {})

        for name, value in kwargs.items():
            setattr(self, name, value)


class FakeEndpoint(RestEndpoint):
    @classmethod
    def extract_request_data(cls, request):
        return request.data


#####################
#       Tests       #
#####################


def test_works_for_query():
    request = FakeRequest()

    args = FakeEndpoint.build_handler_args('query', request)

    assert 'pk' not in args
    assert 'filters' in args


def test_extracts_filters_from_get_params_for_query():
    request = FakeRequest(query={
        'filter1': 'value1',
        'filter2': '123',
        'filter3': '3.14159'
    })

    args = FakeEndpoint.build_handler_args('query', request)

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


def test_works_for_get():
    request = FakeRequest()

    args = FakeEndpoint.build_handler_args('get', request)

    assert args == {}


def test_works_for_create():
    request = FakeRequest(content_type='application/json', data={})

    args = FakeEndpoint.build_handler_args('create', request)

    assert 'pk' not in args
    assert 'data' in args
    assert args['data'] == {}


def test_works_for_update():
    request = FakeRequest(content_type='application/json', data={})

    args = FakeEndpoint.build_handler_args('update', request)

    assert 'data' in args
    assert args['data'] == {}
