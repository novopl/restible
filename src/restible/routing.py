# -*- coding: utf-8 -*-
"""
Helpers for setting up mapping between URLs and resources.
"""
from __future__ import absolute_import, unicode_literals

# 3rd party imports
import attr


@attr.s
class RouteMeta(object):
    """ Route metadata.

    When you have a route function ``my_route`` you can access the metadata
    with ``api_route.get_meta(my_route)``.
    """
    methods = attr.ib()


class api_route(object):
    """ Decorator for defining API routs.

    API routes are endpoints that do not belong to any resource.
    """
    ROUTE_ATTR = '__api_route__'

    def __init__(self, methods=None):
        self.meta = RouteMeta(
            methods=[m.lower() for m in (methods or ['post'])]
        )

    def __call__(self, fn):
        """ Decorator. """
        setattr(fn, self.ROUTE_ATTR, self.meta)
        return fn

    @classmethod
    def get_meta(cls, route):
        """ Get route metadata. """
        return getattr(route, cls.ROUTE_ATTR, {})
