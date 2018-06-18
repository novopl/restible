# -*- coding: utf-8 -*-
"""
webapp2 implementation for the `RestEndpoint`.
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
import json

# 3rd party imports
import webapp2
from six import iteritems

# local imports
from restible import RestEndpoint, RawResponse


class Webapp2Endpoint(webapp2.RequestHandler, RestEndpoint):
    """ Endpoint implementation to use in webapp2/AppEngine projects. """
    def __init__(self, *args, **kw):
        webapp2.RequestHandler.__init__(self, *args, **kw)
        RestEndpoint.__init__(self, self.resource)

    @classmethod
    def extract_request_data(cls, request):
        return json.loads(request.body)

    def response_from_result(self, result):
        """ Generate webapp2 response from  RestResult.

        :param RestResult result:
            RestResult instance with the API call result.
        """
        if isinstance(result, RawResponse):
            pass

        for name, value in iteritems(result.headers):
            self.response.headers[name] = value

        self.response.set_status(result.status)
        self.response.out.write(json.dumps(result.data))

    def dispatch(self):
        """ Override webapp2 dispatcher. """
        request = self.request
        request.rest_keys = request.route_kwargs

        result = self.call_rest_handler(request.method, request)
        return self.response_from_result(result)
