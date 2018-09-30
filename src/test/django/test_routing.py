# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# stdlib imports
import sys

# 3rd party imports
import pytest
from mock import Mock, patch

# local imports
from restible import RestResource
from restible.integrations.django import DjangoEndpoint


#####################
#     Test data     #
#####################


class FakeResource1(RestResource):
    name = 'fake1'


class FakeResource2(RestResource):
    name = 'fake2'


class CustomDjangoEndpoint(DjangoEndpoint):
    pass


urlpatterns = DjangoEndpoint.make_urls([
    ('/fake1', FakeResource1),
    ('/fake2', CustomDjangoEndpoint(FakeResource2)),
])


#####################
#       Tests       #
#####################


@pytest.mark.django
@pytest.mark.urls(__name__)
@pytest.mark.parametrize('method,url,args,verb', (
    ('GET', '/fake1', {}, 'rest_query'),
    ('GET', '/fake1/123', {}, 'rest_get'),
    ('POST', '/fake1', {}, 'rest_create'),
    ('PUT', '/fake1/123', {}, 'rest_update'),
    ('DELETE', '/fake1/123', {}, 'rest_delete'),
    ('HEAD', '/fake1', {}, 'rest_head'),
    ('HEAD', '/fake1/123', {}, 'rest_head'),
    ('OPTIONS', '/fake1', {}, 'rest_options'),
    ('OPTIONS', '/fake1/123', {}, 'rest_options'),
))
def test_all_urls_are_resolved_to_proper_verbs(method, url, args, verb, client):
    with patch.object(FakeResource1, verb) as _handler1:
        with patch.object(FakeResource2, verb) as _handler2:
            _handler1.return_value = {}    # JSON serializable response

            response = client.generic(method, url, **args)

            assert response.status_code < 300
            _handler1.assert_called_once()


@pytest.mark.django
@pytest.mark.urls(__name__)
@patch.object(FakeResource1, 'rest_get', Mock(return_value={}))
@patch.object(FakeResource1, 'rest_query', Mock(return_value={}))
@patch.object(FakeResource2, 'rest_get', Mock(return_value={}))
@patch.object(FakeResource2, 'rest_query', Mock(return_value={}))
@pytest.mark.parametrize('url', (
    '/fake1/',
    '/fake1/123',
    '/fake2/',
    '/fake2/123'
))
def test_combines_urls_from_multiple_endpoints(url, client):
    r = client.get(url)

    assert r.status_code < 300


@pytest.mark.django
@pytest.mark.skipif(sys.version_info < (3, 0),
                    reason="Hacky solution doesn't work in python2")
def test_can_pass_resource_directly():
    urlpatterns = DjangoEndpoint.make_urls([
        ('/fake1', FakeResource1)
    ])

    assert len(urlpatterns) == 2
    assert 'DjangoEndpoint.dispatch' in urlpatterns[0].lookup_str
    assert 'DjangoEndpoint.dispatch' in urlpatterns[1].lookup_str
