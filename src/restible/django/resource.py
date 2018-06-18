# -*- coding: utf-8 -*-
"""
Base class for django based REST resources
"""
from __future__ import absolute_import, unicode_literals

# 3rd party imports
from django.db.utils import IntegrityError
from six import iteritems

# local imports
from restible.core.model import ModelResource


class DjangoResource(ModelResource):
    """ Base class for django based REST resources. """
    def create_item(self, values):
        try:
            return self.model.objects.create(**values)
        except IntegrityError as ex:
            raise ModelResource.AlreadyExists(str(ex))

    def update_item(self, request, values):
        pk = self.get_pk(request)
        return self.model.objects.filter(pk=pk).update(**values)

    def delete_item(self, item):
        item.delete()

    def dbquery(self, request, filters):
        return self.model.objects.filter(**filters)

    def deserialize(self, data):
        """ Convert JSON data into model field types.

        The value returned by this function can be used directly to create new
        instances and update existing ones.
        """
        return {n: self.get_field_value(n, v) for n, v in iteritems(data)}

    def get_field_value(self, name, value):
        """ Coerce value to a model field compatible representation. """
        return value

    def get_requested(self, request):
        """ Get requested item. """
        pk = self.get_pk(request)
        try:
            return self.dbquery(request, {}).get(pk=pk)
        except self.model.DoesNotExist:
            return None
