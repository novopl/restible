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
    def json_response(self, status, data={}):
        return FakeResponse(status=status, data=data)

    def is_http_response(self, result):
        return isinstance(result, FakeResponse)


class ReadOnlyResource(RestResource):
    name = 'read_only'

    def __init__(self):
        super(ReadOnlyResource, self).__init__()
        self.options = True

    def query(self, request, filters):
        return FakeResponse(status=200, safe=False, data=[
            {'id': 123, 'name': 'test_resource'},
            {'id': 321, 'name': 'resource_test'},
        ])

    def get(self, request):
        return {
            'id': request.rest_keys['read_only_pk'],
            'name': 'test_resource'
        }


def test_returns_200_if_everything_is_ok(rf):
    endpoint = FakeEndpoint(ReadOnlyResource)
    request = rf.get('/test')

    response = endpoint.dispatch(request)

    assert response.status_code == 200


@pytest.mark.parametrize('http_method,pk', (
    ('POST', 1234),
    ('PUT', None),
    ('DELETE', None),
))
def test_return_405_if_no_rest_verb_is_matched(http_method, pk, rf):
    # This test should not break on JSON decode error (empty body)
    # because .dispatch() should fail earlier.
    endpoint = FakeEndpoint(ReadOnlyResource)
    request = rf.generic(http_method, '/test')

    response = endpoint.dispatch(request, read_only_pk=pk)

    assert response.status_code == 405


def test_return_405_if_handler_method_is_not_implemented(rf):
    endpoint = FakeEndpoint(ReadOnlyResource)
    request = rf.generic(
        'POST', '/test',
        content_type='application/json',
        data={},
    )

    response = endpoint.dispatch(request)

    assert response.status_code == 405


def test_return_405_if_handler_method_is_not_callable(rf):
    endpoint = FakeEndpoint(ReadOnlyResource)
    request = rf.generic('OPTIONS', '/test')

    response = endpoint.dispatch(request, read_only_pk=123)

    assert response.status_code == 405


def test_returns_FakeResponse_when_handler_returns_dict(rf):
    endpoint = FakeEndpoint(ReadOnlyResource)
    request = rf.get('/test')

    response = endpoint.dispatch(request, read_only_pk=123)

    assert isinstance(response, FakeResponse)


@patch.object(ReadOnlyResource, 'get', Mock(
    return_value=FakeResponse(status=418, data={'detail': 'useless'})
))
def test_returns_the_handler_response_directly_if_its_FakeResponse(rf):
    endpoint = FakeEndpoint(ReadOnlyResource)
    request = rf.get('/test')

    response = endpoint.dispatch(request, read_only_pk=123)

    assert isinstance(response, FakeResponse)
    assert response.status_code == 418
    assert json.loads(response.content.decode('utf-8')) == {
        'detail': 'useless'
    }


def test_returns_400_if_it_cant_extract_filters(rf):
    endpoint = FakeEndpoint(ReadOnlyResource)
    # duplicate filters are not allowed
    request = rf.get('/test?value=first&value=second')

    response = endpoint.dispatch(request)

    assert response.status_code == 400


@patch.object(ReadOnlyResource, 'head', Mock(
    side_effect=RuntimeError('Test handling exceptions in resource handlers')
))
def test_returns_500_if_unhandled_exception_occurs_in_the_handler(rf):
    endpoint = FakeEndpoint(ReadOnlyResource)
    request = rf.head('/test')

    response = endpoint.dispatch(request)

    assert response.status_code == 500


def test_handler_is_called_with_request_as_first_argument(rf):
    endpoint = FakeEndpoint(ReadOnlyResource)

    rest_verb = 'create'
    http_method = 'POST'
    pk = None

    with patch.object(ReadOnlyResource, rest_verb) as _create:
        _create.return_value = {}

        request = rf.generic(http_method, '/test', data={})
        endpoint.dispatch(request, read_only_pk=pk)

        _create.assert_called_once()
        assert _create.call_args[0][0] == request


@pytest.mark.parametrize('rest_verb,http_method,pk', (
    ('get', 'GET', 1234),
    ('query', 'GET', None),
    ('create', 'POST', None),
    ('update', 'PUT', 1234),
    ('delete', 'DELETE', 1234),
))
def test_attaches_keys_to_the_request(rest_verb, http_method, pk, rf):
    endpoint = FakeEndpoint(ReadOnlyResource)

    with patch.object(ReadOnlyResource, rest_verb) as _create:
        _create.return_value = {}

        request = rf.generic(http_method, '/test', data={})
        endpoint.dispatch(request, read_only_pk=pk)

        _create.assert_called_once()
        req = _create.call_args[0][0]
        assert hasattr(req, 'rest_keys')
        assert 'read_only_pk' in req.rest_keys
        assert req.rest_keys['read_only_pk'] == pk
