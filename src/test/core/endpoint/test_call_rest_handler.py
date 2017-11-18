# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# stdlib imports
import json

# 3rd party imports
import pytest
from mock import Mock, patch

# Project imports
from restible import RestEndpoint, RestResource


#####################
#     Test data     #
#####################


class FakeRequest(object):
    def __init__(self, **kwargs):
        self.rest_keys = kwargs.get('rest_keys', {})
        self.body = kwargs.pop('body', '').encode('utf-8')
        self.GET = kwargs.pop('query', {})

        for name, value in kwargs.items():
            setattr(self, name, value)


class FakeResponse(object):
    name = 'fake'

    def __init__(self, **kw):
        attr_map = {
            #  kw         attr
            'status': 'status_code'
        }

        if 'data' in kw:
            kw['content'] = json.dumps(kw['data']).encode('utf-8')

        for name, value in kw.items():
            setattr(self, attr_map.get(name, name), value)


class FakeEndpoint(RestEndpoint):
    @classmethod
    def extract_request_data(cls, request):
        return request.data


class ReadOnlyResource(RestResource):
    name = 'read_only'

    def __init__(self):
        super(ReadOnlyResource, self).__init__()
        self.options = True

    def rest_query(self, request, filters):
        return 200, [
            {'id': 123, 'name': 'test_resource'},
            {'id': 321, 'name': 'resource_test'},
        ]

    def rest_get(self, request):
        return {
            'id': request.rest_keys['read_only_pk'],
            'name': 'test_resource'
        }


#####################
#       Tests       #
#####################


def test_returns_200_if_everything_is_ok():
    endpoint = FakeEndpoint(ReadOnlyResource)

    result = endpoint.call_rest_handler('GET', FakeRequest())

    assert result.status


@pytest.mark.parametrize('http_method,pk', (
    ('POST', 1234),
    ('PUT', None),
    ('DELETE', None),
))
def test_return_405_if_no_rest_verb_is_matched(http_method, pk):
    # This test should not break on JSON decode error (empty body)
    # because .dispatch() should fail earlier.
    endpoint = FakeEndpoint(ReadOnlyResource)
    request = FakeRequest(rest_keys={'read_only_pk': pk})

    result = endpoint.call_rest_handler(http_method, request)

    assert result.status == 405


def test_return_405_if_handler_method_is_not_implemented():
    endpoint = FakeEndpoint(ReadOnlyResource)
    request = FakeRequest(content_type='application/json', data={})

    result = endpoint.call_rest_handler('POST', request)

    assert result.status == 405


def test_return_405_if_handler_method_is_not_callable():
    endpoint = FakeEndpoint(ReadOnlyResource)
    request = FakeRequest(rest_keys={'read_only_pk': 123})

    result = endpoint.call_rest_handler('OPTIONS', request)

    assert result.status == 405


def test_fills_in_the_defaults_if_only_data_is_returned_from_handler():
    endpoint = FakeEndpoint(ReadOnlyResource)

    with patch.object(ReadOnlyResource, 'rest_get') as _get:
        _get.return_value = {'msg': 'hello'}

        request = FakeRequest(rest_keys={'read_only_pk': 123})
        result = endpoint.call_rest_handler('GET', request)

        assert result.status == 200
        assert result.headers == {}
        assert result.data == _get.return_value


def test_fills_in_the_defaults_if_only_status_and_data_is_returned():
    endpoint = FakeEndpoint(ReadOnlyResource)

    with patch.object(ReadOnlyResource, 'rest_get') as _get:
        _get.return_value = (418, {'msg': 'hello'})

        request = FakeRequest(rest_keys={'read_only_pk': 123})
        result = endpoint.call_rest_handler('GET', request)

        assert result.status == _get.return_value[0]
        assert result.headers == {}
        assert result.data == _get.return_value[1]


def test_returns_everything_if_the_handler_returns_full_result():
    endpoint = FakeEndpoint(ReadOnlyResource)

    with patch.object(ReadOnlyResource, 'rest_get') as _get:
        _get.return_value = (418, {'X-Hdr': 'value'}, {'msg': 'hello'})

        request = FakeRequest(rest_keys={'read_only_pk': 123})
        result = endpoint.call_rest_handler('GET', request)

        assert result.status == _get.return_value[0]
        assert result.headers == _get.return_value[1]
        assert result.data == _get.return_value[2]


@patch.object(ReadOnlyResource, 'rest_head', Mock(
    side_effect=RuntimeError('Test handling exceptions in resource handlers')
))
def test_returns_500_if_unhandled_exception_occurs_in_the_handler():
    endpoint = FakeEndpoint(ReadOnlyResource)

    result = endpoint.call_rest_handler('HEAD', FakeRequest())

    assert result.status == 500


def test_handler_is_called_with_request_as_first_argument():
    endpoint = FakeEndpoint(ReadOnlyResource)

    rest_verb = 'rest_create'
    http_method = 'POST'
    pk = None

    with patch.object(ReadOnlyResource, rest_verb) as _create:
        _create.return_value = {}

        request = FakeRequest(data={}, rest_keys={'read_only_pk': pk})
        endpoint.call_rest_handler(http_method, request)

        _create.assert_called_once()
        assert _create.call_args[0][0] == request


@pytest.mark.parametrize('rest_method,http_method,pk', (
    ('rest_get', 'GET', 1234),
    ('rest_query', 'GET', None),
    ('rest_create', 'POST', None),
    ('rest_update', 'PUT', 1234),
    ('rest_delete', 'DELETE', 1234),
))
def test_attaches_keys_to_the_request(rest_method, http_method, pk):
    endpoint = FakeEndpoint(ReadOnlyResource)

    with patch.object(ReadOnlyResource, rest_method) as _rest_method_fn:
        _rest_method_fn.return_value = {}

        request = FakeRequest(rest_keys={'read_only_pk': pk}, data={})

        endpoint.call_rest_handler(http_method, request)

        _rest_method_fn.assert_called_once()
        req = _rest_method_fn.call_args[0][0]
        assert hasattr(req, 'rest_keys')
        assert 'read_only_pk' in req.rest_keys
        assert req.rest_keys['read_only_pk'] == pk
