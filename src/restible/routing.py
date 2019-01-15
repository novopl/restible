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
