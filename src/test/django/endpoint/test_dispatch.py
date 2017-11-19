# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# 3rd party imports
import pytest

# Project imports
from restible import RestResource
from restible.django import DjangoEndpoint


class ReadOnlyResource(RestResource):
    name = 'read_only'

    def __init__(self):
        super(ReadOnlyResource, self).__init__()
        self.options = True

    def rest_query(self, request, params):
        return 200, [
            {'id': 123, 'name': 'test_resource'},
            {'id': 321, 'name': 'resource_test'},
        ]

    def rest_get(self, request, params):
        return {
            'id': request.rest_keys['test_pk'],
            'name': 'test_resource'
        }


@pytest.mark.django
def test_aliased_as_endpoint_call_operator(rf):
    endpoint = DjangoEndpoint(ReadOnlyResource)
    request = rf.get('/test')

    response = endpoint.dispatch(request)

    assert response.status_code == 200
