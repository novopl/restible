# -*- coding: utf-8 -*-
"""
Django implementation of a `RestEndpoint`.
"""
from __future__ import absolute_import, unicode_literals

# 3rd party imports
from django.conf.urls import url
from django.http import HttpResponse, JsonResponse

# local imports
from .. import RestEndpoint


class DjangoEndpoint(RestEndpoint):
    """ Endpoint implementation to use in django projects. """
    
    def __call__(self, *args, **kw):
        """ Django 'calls' views so this is what will be ran by django.

        This should cover the whole request lifecycle.
        """
        return self.dispatch(*args, **kw)

    def is_http_response(self, result):
        return isinstance(result, HttpResponse)

    def json_response(self, status, data=None):
        data = data or {}
        return JsonResponse(status=status, safe=False, data=data)

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
