# -*- coding: utf-8 -*-
"""
Rest endpoint base implementation.

Endpoints take care of interacting with HTTP. They for a bridge between HTTP
requests/responses and the REST resources. They should never be implemented
manually and ideally most apps should not need to subclass those but instead
implement all of their logic in the `RestResource` subclasses.

The code here is just an abstract base that holds the code common to all
endpoints. It is not self sufficient, but only minor web-framework dependent
code is left for the subclasses.
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
import json
from logging import getLogger

# local imports
from .resource import RestResource
from . import filters


L = getLogger(__name__)


class RestEndpoint(object):
    """ Abstract base class for all REST endpoints.

    The endpoint responsibility is to provide a bridge between HTTP and
    `RestResource`.  The latter should never directly deal with HTTP.

    The subclasses must implement the following methods:

    - `is_http_response()`
    - `json_response()`

    """

    def __init__(self, res_cls):
        if self.is_resource(res_cls):
            raise ValueError('res_cls must be a subclass of RestResource')

        self.resource = res_cls()

    def is_resource(self, res_cls):
        """ Check if the given object is a resource class.

        :param type res_cls:
            Object to test.
        :return bool:
            **True** if *res_cls* is a resource class.
        """
        return not (isinstance(res_cls, type) and
                    issubclass(res_cls, RestResource))

    def get_ok_status(self, verb):
        """ Get a valid ok status code for a given rest verb. """
        if verb == 'create':
            return 201
        elif verb == 'delete':
            return 204
        else:
            return 200

    def dispatch(self, request, **keys):
        """ Dispatch the request to the appropriate resource method.

        This should handle both standard REST verbs as well as custom
        actions supported by the resource.

        :param HttpRequest request:
            The HTTP request.
        :param Any pk:
            The primary key for the object. This should be taken from the URL
            and if present it means the detail view was called. Lack of ``pk``.
            indicates that the request was made against the list URL.
        :return RestResponse:
            The ``RestResponse`` received from the resource implementation.
        """
        request.rest_keys = keys

        my_pk = request.rest_keys.get(self.resource.name + '_pk')

        rest_verb = self.determine_rest_verb(request.method, my_pk)
        if rest_verb is None:
            return self.json_response(405)

        handler = getattr(self.resource, rest_verb, None)

        if handler is None or not callable(handler):
            return self.json_response(405)

        try:
            handler_args = self.build_handler_args(rest_verb, request)
            result = handler(request, **handler_args)

            if self.is_http_response(result):
                return result
            else:
                return self.json_response(self.get_ok_status(rest_verb), result)

        except ValueError as ex:
            L.exception('Invalid REST invocation')
            L.error(ex)
            return self.json_response(400, {'detail': str(ex)})

        except NotImplementedError as ex:
            return self.json_response(405, {'detail': str(ex)})

        except Exception as ex:
            L.exception('Unhandled resource exception')
            L.error(ex)
            return self.json_response(500, {'detail': str(ex)})

    def is_http_response(self, result):
        """ Check if the given object is complete HTTP response.

        **Has to be implemented by subclasses.**

        If this method returns False, the *response* will be used to build the
        actual response that is returned to the calling endpoint. Having this
        in a separate method makes it possible to customise this behaviour in
        the subclasses and thus possibly support more web frameworks in the
        future.

        :param Any result:
            Resource handler result. This is what is returned by one of the
            handling methods of a given `RestResource`.
        :return:
            **True** if the response can be directly returned to the calling
            framework, **False** if it's just a data and the actual framework
            specific response has to still be built.
        """
        raise NotImplementedError(
            "RestEndpoint sublasses must implement .is_http_response()"
        )

    def json_response(self, status, data=None):
        """ Return a framework specific HTTP response.

        **Has to be implemented by subclasses.**

        :param int status:
            HTTP status code.
        :param dict|list data:
            Data that will be JSON serialized and sent as the response body.
        :return:
            Framework specific HTTP response object.
        """
        raise NotImplementedError(
            "RestEndpoint sublasses must implement .json_response()"
        )

    @classmethod
    def determine_rest_verb(self, http_method, pk):
        """ Return the REST operation associated with the given HTTP method.

        This is part of the `RestEndpoint` class because this way it becomes
        customisable by subclasses.

        :param str|unicode http_method:
            The HTTP method used for the request.
        :param str|int pk:
            The primary key extracted from the URL template.
        :return str|unicode:
            The REST verb associated with that request. This is also the name
            of the method on `RestResource` that will be called by the endpoint.
        """
        if http_method == 'GET':
            return 'query' if pk is None else 'get'
        elif http_method == 'POST' and pk is None:
            return 'create'
        elif http_method == 'PUT' and pk is not None:
            return 'update'
        elif http_method == 'DELETE' and pk is not None:
            return 'delete'
        elif http_method == 'OPTIONS':
            return 'options'
        elif http_method == 'HEAD':
            return 'head'
        else:
            return None

    @classmethod
    def build_handler_args(self, verb, request):
        """ Build handler invocation arguments.

        The parameters extracted here can be directly passed to the
        `RestResource` handler method for the given REST *verb*.

        This is part of the `RestEndpoint` class because this way it becomes
        customisable by subclasses.

        :param str|unicode verb:
            REST verb/action. This is what the `RestResource` classes abstract.
            Can be one of ``get/query/create/update/delete/options/head``.
        :param HttpRequest request:
            An HTTP request the handler will serve. Handler args are extracted
            from it here.
        :param None|int|str|unicode pk:
            The primary key of a resource that will be modified by request or
            ``None`` if the request is to list handlers. This is most likely
            extracted from the URL template and that's why it's not passed as
            part of the request.
        :return dict:
        """
        handler_args = {}

        if verb in ('create', 'update'):
            try:
                if request.body:
                    body = request.body.decode('utf-8')
                    handler_args['data'] = json.loads(body)
                else:
                    handler_args['data'] = None
            except:
                raise ValueError("Invalid JSON body: '{}'".format(
                    request.body.decode('utf-8')
                ))

        if verb in ('query',):
            handler_args['filters'] = filters.extract(request.GET)

        return handler_args
