# -*- coding: utf-8 -*-
"""
REST resource base class.
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
import inspect
import re

from .routing import api_action


class RestResource(object):
    """ Represents the operations available on the given resource.

    This class should not handle HTTP directly. Rather than that there should
    be a separate implementation that maps HTTP layer onto resources. This way
    we can swap the HTTP layer without reimplementing the resource. This also
    follows SRP.

    If the given `RestResource` subclass doesn't have one of the REST methods
    implemented, the endpoint should return 405 Method not allowed (or 404?)
    """

    _NAME_RE = re.compile(r'^[a-zA-Z_][\w\d_]*$')
    name = None
    parent = None

    def __init__(self):
        self._validate_name(self.name)

    def rest_actions(self):
        """ Return all actions defined on the current resource.

        :return List[function]:
            List of action handlers. To get the metadata for a given *action*
            just use ``api_action.get_meta(action)``
        """
        ATTR = '_actions'

        if not hasattr(self, ATTR):
            actions = []
            for _, method in inspect.getmembers(self, inspect.ismethod):
                if api_action.is_action(method):
                    actions.append(method)

            setattr(self, ATTR, actions)

        return getattr(self, ATTR)

    def get_pk(self, request):
        """ Read the current resource type PK from the request.

        :param HttpRequest request:
            An HTTP request. Must contain the ``.rest_keys`` dictionary injected
            by `RestEndpoint.dispatch()` method.
        :return:
            Primary key that is associated with this resource type. This is
            extracted from ``.rest_keys`` based on the resource name.
        """
        if hasattr(request, 'rest_keys'):
            return request.rest_keys.get(self.name + '_pk')

    def _validate_name(self, name):
        """ Validate the name is a valid resource name. """
        if name is None or not self._NAME_RE.match(name):
            raise ValueError(
                'REST endpoint name contain only letters, digits and '
                'underscores and cannot start with a digit'
            )

    def get_requested(self, request):
        """ Get an item associated with the request.

        This is used by all detail views/actions to get the item that the
        request is concerned with (usually from the URL). This is an
        implementation detail and is highly dependant on the underlying web
        framework used.

        :param request:
            HTTP request.
        :return RestResource:
            The item associated with the request.
        """
        raise NotImplementedError("{}.get_requested() not implemented".format(
            self.__class__.__name__
        ))

    def rest_query(self, request, params):
        """ GET list. """
        raise NotImplementedError(".rest_query() not implemented".format(
            self.__class__.__name__
        ))

    def rest_get(self, request, params):
        """ GET detail. """
        raise NotImplementedError("{}.rest_get() not implemented".format(
            self.__class__.__name__
        ))

    def rest_create(self, request, data):
        """ POST list. """
        raise NotImplementedError("{}.rest_create() not implemented".format(
            self.__class__.__name__
        ))

    def rest_update(self, request, data):
        """ PUT detail. """
        raise NotImplementedError("{}.rest_update() not implemented".format(
            self.__class__.__name__
        ))

    def rest_delete(self, request):
        """ DELETE detail. """
        raise NotImplementedError("{}.rest_delete() not implemented".format(
            self.__class__.__name__
        ))

    def rest_options(self, request):
        """ OPTIONS list/detail. """
        raise NotImplementedError("{}.rest_options() not implemented".format(
            self.__class__.__name__
        ))

    def rest_head(self, request):
        """ OPTIONS list/detail. """
        raise NotImplementedError("{}.rest_head() not implemented".format(
            self.__class__.__name__
        ))
