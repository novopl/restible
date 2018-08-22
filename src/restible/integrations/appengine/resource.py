# -*- coding: utf-8 -*-
"""
Base class for resources using Google AppEngine ndb as storage.
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
from logging import getLogger

# 3rd party imports
from serafin import Fieldspec
from six import iteritems

# local imports
from restible.core.model import ModelResource


L = getLogger(__name__)


class NdbResource(ModelResource):
    """ Base class for ndb based resources.

    This provides a basic implementation that can be used out of the box. It
    provides no authentication/authorization.
    """
    name = None
    model = None
    spec = Fieldspec('*')
    schema = {}

    def create_item(self, values):
        item = self.model(**values)
        item.put()

        return item

    def update_item(self, request, values):
        item = self.get_requested(request)

        if item is None:
            return None

        for name, value in iteritems(values):
            if name not in ('id',):
                try:
                    setattr(item, name, value)
                except AttributeError:
                    L.exception("Failed to set attribute '{}'".format(name))
                    raise

        item.put()

        return item

    def delete_item(self, item):
        item.delete()

    def dbquery(self, request, filters):
        """ Return a model query with the given filters.

        The query can be further customised like any ndb query.

        :return google.appengine.ext.ndb.Query:
            The query with the given filters already applied.
        """
        filters = [getattr(self.model, n) == v for n, v in iteritems(filters)]
        return self.model.query().filter(*filters)

    def get_requested(self, request):
        pk = self.get_pk(request)
        return self.model.get_by_id(pk)
