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
from collections import namedtuple
from logging import getLogger

# local imports
from .resource import RestResource
from .routing import api_action
from . import params


L = getLogger(__name__)
RestResult = namedtuple('RestResult', 'status,headers,data')


class RawResponse(object):
    """ Wrapper around raw framework responses.

    This exists so it can help distinguish
    """
    def __init__(self, response):
        self.response = response


class RestEndpoint(object):
    """ Abstract base class for all REST endpoints.

    The endpoint responsibility is to provide a bridge between HTTP and
    `RestResource`.  The latter should never directly deal with HTTP.


    :param RestResource resource:
        `RestResource` instance. This supersedes whatever is passed in
        `res_cls`.
    :param type res_cls:
        Class derived from `RestResource`. If `resource` is not passed
        directly you can also specify the resource class. It will be used
        to instantiate the resource when the endpoint is created.
    :param bool protected:
        If set to *True*, all CRUD operations on the endpoint will require
        authorization.
    """

    def __init__(self, resource=None, res_cls=None, protected=False):
        resource = resource or getattr(self, 'resource', None)
        res_cls = res_cls or getattr(self, 'res_cls', None)

        if resource is not None and isinstance(resource, RestResource):
            self.resource = resource
        elif (
                res_cls is not None and
                isinstance(res_cls, type) and
                issubclass(res_cls, RestResource)
        ):
            self.resource = res_cls()
        else:
            raise ValueError(
                "You must specify the resource either as a static variable "
                "resource or res_cls or through corresponding constructor "
                "args"
            )

        self.protected = protected

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

    def authorize(self, request):
        """ Authorize user from request.

        By default it returns None, so no user. Treat it as unauthorized

        :param request:
            HTTP request.
        :return:
            A user instance (depending on the underlying storage/models) or None
            if not authorized.
        """
        return None

    def process_result(self, result, default_status):
        """ Unify the handler result into a stable format.

        The unified format is ``(status, headers, data)``.

        :param tuple|dict|list result:
            The result as returned from the handler
        :param int default_status:
            Default HTTP status to use (if result contains none).
        :return tuple(int, dict, dict):
            Tuple . The handlers can return data in
            the shortened forms, either ``(status, data)`` or just ``data``.
            This method will expand those results with default and return a
            unified result tuple.
        """
        status = default_status
        headers = {}
        data = None

        if isinstance(result, tuple):
            if len(result) == 2:
                status, data = result
            elif len(result) == 3:
                status, headers, data = result

        elif isinstance(result, RawResponse):
            return result

        else:
            data = result

        return RestResult(status, headers, data)

    def call_rest_handler(self, method, request):
        """

        :param str method:
            HTTP method. Must be uppercase
        :param request:
            HTTP request. It is assumed the request object hast the following
            members: ``rest_keys``,
        :return tuple(int, dict, dict):
            Tuple ``(status, headers, data)``. The handlers can return data in
            the shortened forms, either ``(status, data)`` or just ``data``.
            This method will expand those results with default and return a
            unified result tuple.
        """
        my_pk = self.resource.get_pk(request)

        request.user = self.authorize(request)
        if self.protected and request.user is None:
            return RestResult(401, {}, {'detail': "Not Authorized"})

        rest_verb = self.determine_rest_verb(method, my_pk)
        if rest_verb is None:
            return RestResult(405, {}, None)

        handler = getattr(self.resource, 'rest_' + rest_verb, None)
        if handler is None or not callable(handler):
            return RestResult(405, {}, None)

        try:
            handler_args = self.build_handler_args(rest_verb, request)
            result = handler(request, **handler_args)
            return self.process_result(result, self.get_ok_status(rest_verb))

        except ValueError as ex:
            L.exception('Invalid REST invocation')
            L.error(ex)
            return RestResult(400, {}, {'detail': str(ex)})

        except NotImplementedError as ex:
            return RestResult(405, {}, {'detail': str(ex)})

        except Exception as ex:
            L.exception('Unhandled resource exception')
            L.error(ex)
            return RestResult(500, {}, {'detail': str(ex)})

    def call_action_handler(self, method, request, name, is_generic):
        """ Call an action on the bound resource.

        :param request:
            HTTP request that called the action.
        :param str name:
            The action name.
        :param bool is_generic:
            True if we should call a generic actions. Generic actions are
            executed globally for the resource. Non-generic actions are called
            on one specific resource instance.
        :return RestResult:
            RestResult tuple with the result of the REST call. This can be
            easily converted to any underlying framework.
        """
        action = self.find_action(name, is_generic)
        if action is None:
            return RestResult(404, {}, {'detail': "{} has no action: {}".format(
                self.resource.name, name
            )})

        meta = api_action.get_meta(action)
        user = self.authorize(request)

        if meta.protected and user is None:
            return RestResult(401, {}, {'detail': "Not Authorized"})

        if method.lower() not in meta.methods:
            return RestResult(405, {}, {
                'detail': "Action {}.{} does not support method {}".format(
                    self.resource.__class__.__name__, meta.name, method.upper()
                )
            })

        request.user = user
        payload = self.extract_request_data(request)
        qs = self.extract_request_query_string(request)
        action_params = params.parse(qs)
        result = action(request, action_params, payload)

        return self.process_result(result, 200)

    def find_action(self, name, generic):
        """ Find API action by name and kind.

        :param str name:
            The action name.
        :param bool is_generic:
            True if we should call a generic actions. Generic actions are
            executed globally for the resource. Non-generic actions are called
            on one specific resource instance.
        :return Function:
            Action handler with it's associated metadata. THe metadata can
            be accessed using ``api_action.get_meta(action)``
        """
        for action in self.resource.rest_actions():
            meta = api_action.get_meta(action)

            if meta.name == name and meta.generic == generic:
                return action

        return None

    def call_action(self, request, action):
        """ Call API action. """
        payload = self.extract_request_data(request)
        qs = self.extract_request_query_string(request)
        action_params = params.parse(qs)

        L.info("Calling action {}".format(action))
        return action(request, action_params, payload)

    @classmethod
    def determine_rest_verb(cls, http_method, pk):
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
    def extract_request_data(cls, request):
        """ Extract request data as a python data structure

        This method is here to provide an easy way to implement new framework
        support. The way the request data is handled is framework dependant
        so each endpoint implementation for the given framework must provide
        and implementation of this function.

        :param Request request:
            Underlying framework dependant request.
        :return:
            A python data structure (dict,list,string, primitive type) that is
            the request data extract from the underlying
        """
        raise NotImplementedError(
            "RestEndpoint sublasses must implement .extract_request_data()"
        )

    @classmethod
    def extract_request_query_string(cls, request):
        """ Extract request params as a python dictionary.

        This method is here to provide an easy way to implement new framework
        support. The way the request params are handled is framework dependant
        so each endpoint implementation for the given framework must provide
        an implementation of this function.

        :param Request request:
            Underlying framework dependant request.
        :return:
            A python dict with ``{name: value}`` pairs for all request query
            string params
        """
        return request.GET

    @classmethod
    def build_handler_args(cls, verb, request):
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
            handler_args['data'] = cls.extract_request_data(request)

        if verb in ('query', 'get'):
            qs = cls.extract_request_query_string(request)
            handler_args['params'] = params.parse(qs)

        return handler_args