# -*- coding: utf-8 -*-
"""
Base class for resources using Google AppEngine ndb as storage.
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
from logging import getLogger

# 3rd party imports
from six import iteritems

# local imports
from restible import Fieldspec
from restible.core.model import ModelResource


L = getLogger(__name__)


class SqlAlchemyResource(ModelResource):
    """ Base class for ndb based resources.

    This provides a basic implementation that can be used out of the box. It
    provides no authentication/authorization.
    """
    name = None
    model = None
    spec = Fieldspec('*')
    schema = {}
    read_only = []
    _public_props = None

    @classmethod
    def init_app(cls, db):
        """ Initialize SQLAlchemy resources. """
        cls._db = db

    def create_item(self, values):
        """ Create new model item. """
        item = self.model(**values)
        self._db.session.add(item)
        self._db.session.commit()

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

        self._db.session.commit()

    def delete_item(self, item):
        self._db.session.delete(item)
        self._db.session.commit()

    def deserialize(self, data):
        """ Convert JSON data into model field types.

        The value returned by this function can be used directly to create new
        item and update existing ones.
        """
        return {n: self.get_field_value(n, v) for n, v in iteritems(data)}

    def get_field_value(self, name, value):
        """ Coerce value to a model field compatible representation. """
        return value

    def dbquery(self, filters):
        """ Return a model query with the given filters.

        The query can be further customised like any ndb query.

        :return google.appengine.ext.ndb.Query:
            The query with the given filters already applied.
        """
        filters = [getattr(self.model, n) == v for n, v in iteritems(filters)]
        return self.model.query.filter(*filters).all()

    def get_requested(self, request):
        """ Get requested item. """
        pk = self.get_pk(request)
        return self.model.query.get(pk)
