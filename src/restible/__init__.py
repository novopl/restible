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
Simple REST API implementation.

Each endpoint has it's resource class that represents all the operations
possible in that endpoint. The resource implementation should be framework
agnostic so it can be used both on AppEngine and regular django (possibly other
frameworks as well..
"""
from __future__ import absolute_import, unicode_literals

# package interface
from .endpoint import RestEndpoint, RawResponse
from .exc import Error
from .exc import BadRequest
from .exc import NotAllowed
from .exc import NotAuthorized
from .exc import NotFound
from .model import ModelResource
from .resource import RestResource
from .actions import api_action
from .routing import api_route

__version__ = '0.11.2'

__all__ = [
    'api_action',
    'api_route',
    'ModelResource',
    'RawResponse',
    'RestEndpoint',
    'RestResource',
]
