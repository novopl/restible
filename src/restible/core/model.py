# -*- coding: utf-8 -*-
""" Base class for resources based on DB models. """
from __future__ import absolute_import, unicode_literals

# stdlib imports
from logging import getLogger

# 3rd party imports
from jsonschema import validate, ValidationError
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
            validate(data, schema or self.schema)
        except ValidationError as ex:
            raise ModelResource.ValidationError(ex)

    def serialize(self, item_or_items):
        """ Serialize an item or items into a dict.

        This will just call serafin.serialize using the model spec (defined
        class wide in the model - '*' by default).

        :param item_or_items:
        :return Dict[Any, Any]:
            A dict with python native content. Can be easily dumped to any
            format like JSON or YAML.
        """
        return serialize(item_or_items, self.spec)

    def deserialize(self, data):
        """ Convert JSON data into model field types.

        The value returned by this function can be used directly to create new
        item and update existing ones.
        """
        return {n: self.get_field_value(n, v) for n, v in iteritems(data)}

    def get_field_value(self, name, value):
        """ Coerce value to a model field compatible representation. """
        return value

    @property
    def public_props(self):
        """ All public properties on the resource model. """
        if self._public_props is None:
            self._public_props = [
                name for name, _ in iter_public_props(self.model)
            ]
        return self._public_props

    def create_item(self, values):
        """ Create new model item. """
        raise NotImplementedError("Must implement .create_item()")

    def update_item(self, request, values):
        """ Update existing model item. """
        raise NotImplementedError("Must implement .update_item()")

    def delete_item(self, item):
        """ Update existing model item. """
        raise NotImplementedError("Must implement .delete_item()")

    def dbquery(self, request, filters):
        """ Return a model query with the given filters.

        The query can be further customised like any ndb query.

        :return google.appengine.ext.ndb.Query:
            The query with the given filters already applied.
        """
        raise NotImplementedError("Must implement .dbquery()")

    def get_requested(self, request):
        """ Get requested item. """
        raise NotImplementedError("Must implement .get_requested()")

    def rest_query(self, request, params):
        """ Query existing records as a list. """
        try:
            fields = params.pop('_fields', '*')

            filters = self.deserialize(params)
            items = self.dbquery(request, filters)

            spec = Fieldspec(self.spec).restrict(Fieldspec(fields))
            ret = serialize(items, spec)
            return 200, ret

        except NotImplementedError:
            return 405, {'detail': 'Method not allowed'}

    def rest_create(self, request, data):
        """ Create a new record. """
        try:
            self.validate(data, self.schema)

            values = self.deserialize(data)
            item = self.create_item(values)

            return serialize(item, self.spec)

        except ModelResource.ValidationError as ex:
            return 400, {'detail': str(ex)}

        except ModelResource.AlreadyExists:
            return 400, {'detail': 'Already exists'}

        except NotImplementedError:
            return 405, {'detail': 'Method not allowed'}

    def rest_get(self, request, params):
        """ Get one record with the given id. """
        try:
            fields = Fieldspec(params.get('_fields', '*'))

            spec = Fieldspec(self.spec).restrict(fields)
            item = self.get_requested(request)

            if item is not None:
                return 200, serialize(item, spec)
            else:
                return 404, {'detail': "Not found"}

        except NotImplementedError:
            return 405, {'detail': 'Method not allowed'}

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
                return 200, serialize(item, self.spec)
            else:
                return 404, {'detail': "Not Found"}

        except ModelResource.ValidationError as ex:
            return 400, {'detail': str(ex)}

        except NotImplementedError:
            return 405, {'detail': 'Method not allowed'}

    def rest_delete(self, request):
        """ DELETE detail. """
        try:
            item = self.get_requested(request)

            if item is None:
                return 404, {'detail': 'Item does not exist'}

            self.delete_item(item)

            return 204, {}

        except NotImplementedError:
            return 405, {'detail': 'Method not allowed'}
