# -*- coding: utf-8 -*-
"""
Django implementation of a `RestEndpoint`.
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
import json

# 3rd party imports
from django.conf.urls import url
from django.http import JsonResponse
from six import iteritems

# local imports
from .. import RestEndpoint


class DjangoEndpoint(RestEndpoint):
    """ Endpoint implementation to use in django projects. """
    
    def dispatch(self, request, **keys):
        """ Django 'calls' views so this is what will be ran by django.

        This should cover the whole request lifecycle.
        """
        request.rest_keys = keys

        result = self.call_rest_handler(request.method, request)

        response = JsonResponse(
            status=result.status,
            safe=False,
            data=result.data
        )
        for key, value in iteritems(result.headers):
            response[key] = value

        return response

    @classmethod
    def extract_request_data(cls, request):
        try:
            if request.body:
                body = request.body.decode('utf-8')
                return json.loads(body)
            else:
                return None
        except:
            raise ValueError("Invalid JSON body: '{}'".format(
                request.body.decode('utf-8')
            ))

    @property
    def urls(self):
        """ Return all the URLs required by the endpoint.

        :return list<url>:
            A list of URLs that can be directly appended to ``urlpatterns`` of
            choice.
        """
        # TODO: Using resource.name for both prefix and PK name might blow up.
        # There might be one generic endpoint called /bars and we might want to
        # create a nested one /foo/bars. In those cases we have two resources
        # with the same name - bars.
        #
        # Another question is whether this is an issue. In the above example
        # the resources are not at the same 'level' in the tree. This will
        # definitely fail if we have a recursive endpoint, but that might be
        # even worse.
        name = self.resource.name
        ret = [
            url(
                '{name}/(?P<{name}_pk>[^/]+)/?$'.format(name=name),
                self.dispatch,
                name='{name}-detail'.format(name=name)
            ),
            url(
                '{name}/?$'.format(name=name),
                self.dispatch,
                name='{name}-list'.format(name=name)
            ),
        ]
        return ret
