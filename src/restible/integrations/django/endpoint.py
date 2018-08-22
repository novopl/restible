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
from restible import api_action, RestEndpoint, RestResource, RawResponse


class DjangoEndpoint(RestEndpoint):
    """ Endpoint implementation to use in django projects. """

    def dispatch(self, request, **route_params):
        """ Django 'calls' views so this is what will be ran by django.

        This should cover the whole request lifecycle.
        """
        request.rest_keys = route_params

        result = self.call_rest_handler(request.method, request)
        return self.response_from_result(result)

    def dispatch_action(self, request, name, generic, **route_params):
        """ Dispatch resource action. """
        request.rest_keys = route_params

        result = self.call_action_handler(request, name, generic)
        return self.response_from_result(result)

    def response_from_result(self, result):
        """ Create django response from RestResult.

        :param RestResult result:
        :return JsonResponse:
            Django response instance, ready to return from the view.
        """
        if isinstance(result, RawResponse):
            return result.response

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

    @classmethod
    def extract_request_query_string(cls, request):
        return request.GET

    def urls(self, base_url):
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
        if base_url.endswith('/'):
            base_url = base_url[:-1]

        if base_url.startswith('/'):
            base_url = base_url[1:]

        name = self.resource.name
        list_url = base_url
        item_url = '{url}/(?P<{name}_pk>[^/]+)'.format(url=base_url, name=name)
        routes = []

        # actions
        for action in self.resource.rest_actions():
            meta = api_action.get_meta(action)
            route_name = '{}-{}'.format(self.resource.name, meta.name),
            action_url = '{url}/{action}'.format(
                url=list_url if meta.generic else item_url,
                action=meta.name
            )

            routes.append(
                url(action_url, self.dispatch_action, name=route_name, kwargs={
                    'name': meta.name,
                    'generic': meta.generic,
                })
            )

        routes += [
            url(item_url, self.dispatch, name='{name}-item'.format(name=name)),
            url(list_url, self.dispatch, name='{name}-list'.format(name=name)),
        ]

        return routes

    @classmethod
    def make_urls(cls, routes):
        """ Create a list of URLs handled by this endpoint. """
        urlconf = []

        for entry in routes:
            endpoint = None
            opts = {}

            if len(entry) == 2:
                url, res_cls = entry
            else:
                url, res_cls, opts = entry

            if isinstance(res_cls, type) and issubclass(res_cls, RestResource):
                endpoint = cls(res_cls, **opts)
            elif isinstance(res_cls, RestEndpoint):
                endpoint = res_cls
            else:
                raise RuntimeError("Invalid resource class for {}".format(
                    res_cls.name
                ))

            urlconf += endpoint.urls(url)

        return urlconf
