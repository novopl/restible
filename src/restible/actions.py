# -*- coding: utf-8 -*-
# Copyright 2017-2019 Mateusz Klos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
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
    schema = attr.ib()


class api_action(object):
    """ Decorator for defining resource actions.

    Actions are extra HTTP endpoints that can be called with POST.
    """
    ACTION_ATTR = '__api_action__'

    def __init__(self, name=None, generic=False, protected=True, methods=None,
                 schema=None):
        self.name = name
        self.generic = generic
        self.protected = protected
        self.schema = schema
        self.methods = [m.lower() for m in (methods or ['post'])]

    def __call__(self, fn):
        """ Decorator. """
        setattr(fn, self.ACTION_ATTR, ActionMeta(
            name=self.name or fn.__name__,
            generic=self.generic,
            protected=self.protected,
            methods=self.methods,
            schema=self.schema,
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
