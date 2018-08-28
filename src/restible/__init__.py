# -*- coding: utf-8 -*-
"""
Simple REST API implementation.

Each endpoint has it's resource class that represents all the operations
possible in that endpoint. The resource implementation should be framework
agnostic so it can be used both on AppEngine and regular django (possibly other
frameworks as well..
"""
from __future__ import absolute_import, unicode_literals

# package interface
from .core.endpoint import RestEndpoint, RawResponse
from .core.model import ModelResource
from .core.resource import RestResource
from .core.routing import api_action
from .core.routing import api_route

__version__ = '0.3.2'

__all__ = [
    'api_action',
    'api_route',
    'ModelResource',
    'RawResponse',
    'RestEndpoint',
    'RestResource',
]
