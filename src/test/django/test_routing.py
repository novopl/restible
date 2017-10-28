# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# 3rd party imports
import pytest
from mock import Mock, patch

# local imports
from restible import RestResource
from restible.django import DjangoEndpoint
from restible.core.routing import make_urls


class FakeResource1(RestResource):
    name = 'fake1'


class FakeResource2(RestResource):
    name = 'fake2'


class CustomDjangoEndpoint(DjangoEndpoint):
    pass


urlpatterns = make_urls(DjangoEndpoint, [
    FakeResource1,
    CustomDjangoEndpoint(FakeResource2),
])


@pytest.mark.urls(__name__)
@pytest.mark.parametrize('method,url,args,verb', (
    ('GET', '/fake1/', {}, 'query'),
    ('GET', '/fake1/123', {}, 'get'),
    ('POST', '/fake1/', {}, 'create'),
    ('PUT', '/fake1/123', {}, 'update'),
    ('DELETE', '/fake1/123', {}, 'delete'),
    ('HEAD', '/fake1/', {}, 'head'),
    ('HEAD', '/fake1/123', {}, 'head'),
    ('OPTIONS', '/fake1/', {}, 'options'),
    ('OPTIONS', '/fake1/123', {}, 'options'),
))
def test_all_urls_are_resolved_to_proper_verbs(method, url, args, verb, client):
    with patch.object(FakeResource1, verb) as _handler1:
        with patch.object(FakeResource2, verb) as _handler2:
            _handler1.return_value = {}    # JSON serializable response

            response = client.generic(method, url, **args)

            assert response.status_code < 300
            _handler1.assert_called_once()


@pytest.mark.urls(__name__)
@patch.object(FakeResource1, 'get', Mock(return_value={}))
@patch.object(FakeResource1, 'query', Mock(return_value={}))
@patch.object(FakeResource2, 'get', Mock(return_value={}))
@patch.object(FakeResource2, 'query', Mock(return_value={}))
@pytest.mark.parametrize('url', (
    '/fake1/',
    '/fake1/123',
    '/fake2/',
    '/fake2/123'
))
def test_combines_urls_from_multiple_endpoints(url, client):
    r = client.get(url)

    assert r.status_code < 300


def test_can_pass_resource_directly():
    urlpatterns = make_urls(DjangoEndpoint, [
        FakeResource1,
    ])

    assert len(urlpatterns) == 2
    assert urlpatterns[0].lookup_str.endswith('RestEndpoint.dispatch')
    assert urlpatterns[1].lookup_str.endswith('RestEndpoint.dispatch')
