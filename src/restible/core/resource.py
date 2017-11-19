# -*- coding: utf-8 -*-
"""
REST resource base class.
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
import re


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

    def _validate_name(self, name):
        """ Validate the name is a valid resource name. """
        if name is None or not self._NAME_RE.match(name):
            raise ValueError(
                'REST endpoint name contain only letters, digits and '
                'underscores and cannot start with a digit'
            )

    def rest_query(self, request, params):
        """ GET list. """
        raise NotImplementedError("query() not implemented by this resource")

    def rest_get(self, request, params):
        """ GET detail. """
        raise NotImplementedError("get() not implemented by this resource")

    def rest_create(self, request, data):
        """ POST list. """
        raise NotImplementedError("create() not implemented by this resource")

    def rest_update(self, request, data):
        """ PUT detail. """
        raise NotImplementedError("update() not implemented by this resource")

    def rest_delete(self, request):
        """ DELETE detail. """
        raise NotImplementedError("delete() not implemented by this resource")

    def rest_options(self, request):
        """ OPTIONS list/detail. """
        raise NotImplementedError("options() not implemented by this resource")

    def rest_head(self, request):
        """ OPTIONS list/detail. """
        raise NotImplementedError("options() not implemented by this resource")

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
