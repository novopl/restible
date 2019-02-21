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
""" Base class for resources based on DB models. """
from __future__ import absolute_import, unicode_literals

# stdlib imports
from logging import getLogger
from typing import Text

# 3rd party imports
import jsonschema
from serafin import Fieldspec, serialize
from six import iteritems

# local imports
from .resource import RestResource
from .util import iter_public_props


L = getLogger(__name__)


class ModelResource(RestResource):
    """ Base class for resources based on DB models. """

    model = None
    spec = Fieldspec('*')
    schema = {}
    read_only = []

    class AlreadyExists(RuntimeError):
        """ Raised when an object already exists. """
        pass

    class ValidationError(RuntimeError):
        """ Raised by .validate() if it fails. """
        def __init__(self, jsonschema_error):
            self.detail = jsonschema_error
            super(ModelResource.ValidationError, self).__init__(
                str(jsonschema_error)
            )

    def validate(self, data, schema=None):
        """ Validate the *data* according to the given *schema*.

        :param Dict[str, Any] data:
            A dictionary of data. Probably coming from the user in some way.
        :param Dict[str, Any] schema:
            JSONSchema describing the required data structure.
        :raises ModelResource.ValidationError:
            If the validation fails. No value is returned.
        """
        try:
            jsonschema.validate(data, schema or self.schema)
        except jsonschema.ValidationError as ex:
            raise ModelResource.ValidationError(ex)

    def serialize(self, item_or_items, spec=None):
        """ Serialize an item or items into a dict.

        This will just call serafin.serialize using the model spec (defined
        class wide in the model - '*' by default).

        :param item_or_items:
        :return Dict[Any, Any]:
            A dict with python native content. Can be easily dumped to any
            format like JSON or YAML.
        """
        if spec is None:
            spec = self.spec

        return serialize(item_or_items, spec)

    def deserialize(self, data):
        """ Convert JSON data into model field types.

        The value returned by this function can be used directly to create new
        item and update existing ones.
        """
        return {n: self.get_field_value(n, v) for n, v in iteritems(data)}

    def get_field_value(self, name, value):
        """ Coerce value to a model field compatible representation. """
        return value

    def implements(self, rest_verb):
        # type: (Text) -> bool
        """ Check whether this model resource implements a given REST verb.

        Args:
            rest_verb (str):
                The REST verb you want to check. Possible values are *create*,
                *query*, *get*, *update* and *delete*.

        Returns:
            bool: **True** if the given REST verb is implemented, **False**
                otherwise.
        """
        test = {
            'create': lambda: self.create_item(None, {}),
            'query': lambda: self.query_items(None, {}),
            'get': lambda: self.get_item(None),
            'update': lambda: self.update_item(None, {}),
            'delete': lambda: self.delete_item(None, {}),
        }.get(rest_verb)

        if test:
            try:
                test()
                return True
            except NotImplementedError:
                return False
            except:
                return True
        else:
            return False

    @property
    def public_props(self):
        """ All public properties on the resource model. """
        if not hasattr(self, '_public_props'):
            self._public_props = [
                name for name, _ in iter_public_props(self.model)
            ]
        return self._public_props

    def create_item(self, request, values):
        """ Create new model item. """
        raise NotImplementedError("Must implement .create_item()")

    def update_item(self, request, values):
        """ Update existing model item. """
        raise NotImplementedError("Must implement .update_item()")

    def delete_item(self, request, item):
        """ Delete model instance. """
        raise NotImplementedError("Must implement .delete_item()")

    def query_items(self, request, filters):
        """ Return a model query with the given filters.

        The query can be further customised like any ndb query.

        :return google.appengine.ext.ndb.Query:
            The query with the given filters already applied.
        """
        raise NotImplementedError("Must implement .query_items()")

    def get_item(self, request):
        """ Get an item associated with the request.

        This is used by all detail views/actions to get the item that the
        request is concerned with (usually from the URL). This is an
        implementation detail and is highly dependant on the underlying web
        framework used.

        :param request:
            HTTP request.
        :return RestResource:
            The item associated with the request.
        """
        raise NotImplementedError("{}.get_item() not implemented".format(
            self.__class__.__name__
        ))

    def rest_query(self, request, params):
        """ Query existing records as a list. """
        try:
            fields = params.pop('_fields', '*')

            filters = self.deserialize(params)
            items = self.query_items(request, filters)

            spec = Fieldspec(self.spec).restrict(Fieldspec(fields))
            ret = self.serialize(items, spec)
            return 200, ret

        except NotImplementedError:
            return 404, {'detail': 'Not Found'}

    def rest_create(self, request, data):
        """ Create a new record. """
        try:
            self.validate(data, self.schema)

            values = self.deserialize(data)
            item = self.create_item(request, values)

            return self.serialize(item)

        except ModelResource.ValidationError as ex:
            return 400, {'detail': str(ex)}

        except ModelResource.AlreadyExists:
            return 400, {'detail': 'Already exists'}

        except NotImplementedError:
            return 404, {'detail': 'Not Found'}

    def rest_get(self, request, params):
        """ Get one record with the given id. """
        try:
            fields = Fieldspec(params.get('_fields', '*'))

            spec = Fieldspec(self.spec).restrict(fields)
            item = self.get_item(request)

            if item is not None:
                return 200, self.serialize(item, spec)
            else:
                return 404, {'detail': "Not Found"}

        except NotImplementedError:
            return 404, {'detail': 'Not Found'}

    def rest_update(self, request, data):
        """ Update existing item. """
        schema = {}
        schema.update(self.schema)

        if 'required' in schema:
            del schema['required']

        try:
            self.validate(data, schema)

            values = self.deserialize(data)
            read_only = frozenset(self.read_only) | frozenset(self.public_props)
            for name in read_only:
                values.pop(name, None)

            item = self.update_item(request, values)

            if item is not None:
                return 200, self.serialize(item)
            else:
                return 404, {'detail': "Not Found"}

        except ModelResource.ValidationError as ex:
            return 400, {'detail': str(ex)}

        except NotImplementedError:
            return 404, {'detail': 'Not Found'}

    def rest_delete(self, request):
        """ DELETE detail. """
        try:
            item = self.get_item(request)

            if item is None:
                return 404, {'detail': 'Not Found'}

            self.delete_item(request, item)

            return 204, {}

        except NotImplementedError:
            return 404, {'detail': 'Not Found'}


# Used only in type hint comments
del Text
