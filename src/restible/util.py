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
from typing import Any, Dict, Text

# 3rd party import
import attr
from six import iteritems     # pylint: disable=wrong-import-order


@attr.s
class QsFilter(object):
    """ A halper class for parsing query string into db filters. """
    name = attr.ib(type=str)
    op = attr.ib(type=str)
    op_fn = attr.ib(type=str)
    value = attr.ib(type=Any)

    @classmethod
    def build(cls, op_map, param_name, param_value):
        # type: (Dict[Text, Text], Text, Any) -> QsFilter
        """

        Args:
            op_map (dict[str, str]):
                Operator map. This maps the query string op to a method that
                will implement this operator on the model.
            param_name (str):
                The field name as passed in the query string parameter.
            param_value (Any):
                The filter value as passed in the query string parameter.

        Returns:
            QsFilter:
                A `QsFilter` instance that can be then called on model class to
                generate the actual query filter.

        Example:

            >>> from restible.util import QsFilter
            >>> # ?name=John&age__gt=18
            >>> params = {'name': 'John', 'age__gt': 18}
            >>> OP_MAP = {
            ...     'eq': '__eq__',
            ...     'ne': '__ne__',
            ...     'lt': '__lt__',
            ...     'gt': '__gt__',
            ...     'le': '__le__',
            ...     'ge': '__ge__',
            ...     'in': 'in_',
            ... }
            >>>
            >>> filters = [
            ...     QsFilter.build(OP_MAP, k, v) for k, v in params.items()
            ... ]

        """
        parts = param_name.rsplit('__', 1)
        if len(parts) == 2:
            name, op = parts
        else:
            op = 'eq'
            name = parts[0]

        rv = cls(name=name, op=op, op_fn=op_map.get(op), value=param_value)

        if not rv.op_fn:
            msg = "Invalid OP: {0.op} in '{0.name} {0.op} {0.value}'"
            raise ValueError(msg.format(rv))

        return rv

    def __call__(self, model_cls):
        field = getattr(model_cls, self.name)
        op_method = getattr(field, self.op_fn)
        return op_method(self.value)


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


# Used only in type hint comments
del Dict, Text
