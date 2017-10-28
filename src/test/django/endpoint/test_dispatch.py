# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# 3rd party imports
from django.http import JsonResponse

# Project imports
from restible import RestResource
from restible.django import DjangoEndpoint


class ReadOnlyResource(RestResource):
    name = 'read_only'

    def __init__(self):
        super(ReadOnlyResource, self).__init__()
        self.options = True

    def query(self, request, filters):
        return JsonResponse(status=200, safe=False, data=[
            {'id': 123, 'name': 'test_resource'},
            {'id': 321, 'name': 'resource_test'},
        ])

    def get(self, request):
        return {
            'id': request.rest_keys['test_pk'],
            'name': 'test_resource'
        }


def test_aliased_as_endpoint_call_operator(rf):
    endpoint = DjangoEndpoint(ReadOnlyResource)
    request = rf.get('/test')

    response = endpoint(request)

    assert response.status_code == 200
