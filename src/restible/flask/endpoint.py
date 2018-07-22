# -*- coding: utf-8 -*-
""" Flask integration. """
from __future__ import absolute_import, unicode_literals

# stdlib imports
import json
from logging import getLogger
from urllib.parse import urljoin

# 3rd party imports
from flask import request
from restible import RestEndpoint

# local imports
from restible import api_action, api_route, RawResponse


L = getLogger(__name__)


class FlaskEndpoint(RestEndpoint):
    """ Endpoint implementation to use in webapp2/AppEngine projects. """
    @classmethod
    def extract_request_data(cls, request):
        return request.json

    @classmethod
    def extract_request_query_string(cls, request):
        return request.args

    def response_from_result(self, result):
        """ Create django response from RestResult.

        :param RestResult result:
        :return (body, status, headers):
            (body, status, header) tuple.
        """
        if isinstance(result, RawResponse):
            return result.response

        return json.dumps(result.data), result.status, result.headers

    def dispatch(self, **route_params):
        """ Override webapp2 dispatcher. """
        request.rest_keys = route_params

        result = self.call_rest_handler(request.method, request)
        return self.response_from_result(result)

    def dispatch_action(self, name, generic, **route_params):
        """ Override webapp2 dispatcher. """
        request.rest_keys = route_params

        result = self.call_action_handler(
            request.method, request, name, generic
        )
        return self.response_from_result(result)

    @classmethod
    def init_app(cls, app, resources=None, routes=None):
        """ Initialize the endpoint configuration for the given flask app. """
        resources = resources or []
        routes = routes or []
        cls.endpoints = []

        for entry in resources:
            opts = {}

            if len(entry) == 2:
                url, res_cls = entry
            else:
                url, res_cls, opts = entry

            endpoint = cls(res_cls, **opts)
            endpoint._register_routes(app, url)

            cls.endpoints.append(endpoint)

        for url, route in routes:
            if url.endswith('/'):
                url = url[:-1]

            meta = api_route.get_meta(route)
            app.add_url_rule(url, view_func=route, methods=meta.methods)

    def _register_routes(self, app, url):
        """ Register all routes for the current endpoint in the flask app. """
        if not url.endswith('/'):
            url += '/'

        url_list = url
        url_item = urljoin(url, '<{name}_pk>/'.format(
            name=self.resource.name
        ))

        # actions
        for action in self.resource.rest_actions():
            meta = api_action.get_meta(action)

            action_route = dict(
                endpoint='{}-{}'.format(self.resource.name, meta.name),
                defaults={
                    'name': meta.name,
                    'generic': meta.generic,
                },
                view_func=self.dispatch_action,
                methods=meta.methods
            )

            base_url = url_list if meta.generic else url_item
            url_action = urljoin(base_url, meta.name)

            app.add_url_rule(url_action, **action_route)

        item_route = dict(
            endpoint='{}-item'.format(self.resource.name),
            view_func=self.dispatch,
            methods=['get', 'put', 'delete']
        )
        list_route = dict(
            endpoint='{}-list'.format(self.resource.name),
            view_func=self.dispatch,
            methods=['get', 'post']
        )

        app.add_url_rule(url_item[:-1], **item_route)
        app.add_url_rule(url_list[:-1], **list_route)
