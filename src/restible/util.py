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
""" Various helpers. """
from __future__ import absolute_import, unicode_literals

# stdlib imports
import inspect

# 3rd party import
from six import iteritems     # pylint: disable=wrong-import-order


def iter_public_props(obj, predicate=None):
    """ Iterate over public properties of an object.

    :param Any obj:
        The object we want to get the properties of.
    :param function predicate:
        Additional predicate to filter out properties we're interested in. This
        function will be called on every property of the object with the
        property name and value as it arguments. If it returns True, the
        property will be yielded by this generator.
    """
    predicate = predicate or (lambda n, v: True)
    obj_type = type(obj)

    if inspect.isclass(obj):
        # This is a class
        for name, value in iteritems(obj.__dict__):
            if isinstance(value, property):
                yield name, value
    else:
        # This is an instance
        for name in dir(obj):
            if name.startswith('_'):
                continue

            member = getattr(obj_type, name)
            if not isinstance(member, property):
                continue

            try:
                value = getattr(obj, name)
                if predicate(name, value):
                    yield name, value
            except AttributeError:
                pass


def update_from_values(obj, values):
    # type: (object, dict) -> None
    """ Update object attributes from a dict of values.

    This is a small helper to update any object with values from a dictionary.

    Args:
        obj (object):
        values (dict[str, Any]):

    Examples:

        >>> from restible import util
        >>>
        >>> class Person(object):
        ...      def __init__(self):
        ...         self.name = 'John'
        ...         self.age = 35
        >>>
        >>> person = Person()
        >>> util.update_from_values(person, {
        ...     'name': 'Dave',
        ...     'age': 28,
        ... })
        >>> person.name
        'Dave'
        >>> person.age
        28

    """
    for name, value in iteritems(values):
        setattr(obj, name, value)
