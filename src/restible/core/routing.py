# -*- coding: utf-8 -*-
"""
Helpers for setting up mapping between URLs and resources.
"""
from __future__ import absolute_import, unicode_literals

# 3rd party imports
import attr


@attr.s
class ActionMeta(object):
    """ Action metadata.

    When you have a action method ``Res.my_action`` you can access the metadata
    with ``api_action.get_meta(Res.my_action)``.
    """
    name = attr.ib()
    generic = attr.ib()
    protected = attr.ib()
    methods = attr.ib()


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
            methods=methods or ['post']
        )

    def __call__(self, fn):
        """ Decorator. """
        setattr(fn, self.ROUTE_ATTR, self.meta)
        return fn

    @classmethod
    def get_meta(cls, route):
        """ Get route metadata. """
        return getattr(route, cls.ROUTE_ATTR, {})


class api_action(object):
    """ Decorator for defining resource actions.

    Actions are extra HTTP endpoints that can be called with POST.
    """
    ACTION_ATTR = '__api_action__'

    def __init__(self, name=None, generic=False, protected=True, methods=None):
        self.name = name
        self.generic = generic
        self.protected = protected
        self.methods = [m.lower() for m in (methods or ['post'])]

    def __call__(self, fn):
        """ Decorator. """
        setattr(fn, self.ACTION_ATTR, ActionMeta(
            name=self.name or fn.__name__,
            generic=self.generic,
            protected=self.protected,
            methods=self.methods,
        ))
        return fn

    @classmethod
    def is_action(cls, obj):
        """ Return true if obj is an API action. """
        return hasattr(obj, cls.ACTION_ATTR)

    @classmethod
    def get_meta(cls, action):
        """ Get action metadata """
        return getattr(action, cls.ACTION_ATTR, {})
