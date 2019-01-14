# -*- coding: utf-8 -*-
""" Resource actions helpers """
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
    action = attr.ib()


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
            action=fn,
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