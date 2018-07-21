# -*- coding: utf-8 -*-
"""
Base class for resources using Google AppEngine ndb as storage.
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
from logging import getLogger

# 3rd party imports
from six import iteritems
from serafin import Fieldspec
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# local imports
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
    _db_session = None

    @classmethod
    def init_session(cls, db_session):
        """ Initialize SQLAlchemy resources. """
        cls._db_session = db_session

    @property
    def db_session(self):
        """ Property returning the current SQLAlchemy session.

        Will try to get it from ``self.model.query.session`` as this is where
        flask has it.
        """
        if hasattr(self.model, 'query'):
            return self.model.query.session
        else:
            return self._db_session

    def create_item(self, values):
        """ Create new model item. """
        try:
            item = self.model(**values)

            self.db_session.add(item)
            self.db_session.commit()

            return item
        except IntegrityError:
            self.db_session.rollback()
            raise ModelResource.AlreadyExists()
        except SQLAlchemyError:
            self.db_session.rollback()
            raise

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

        try:
            self.db_session.commit()
        except SQLAlchemyError:
            self.db_session.rollback()
            raise

        return item

    def delete_item(self, item):
        try:
            self.db_session.delete(item)
            self.db_session.commit()
        except SQLAlchemyError:
            self.db_session.rollback()
            raise

    def dbquery(self, request, filters):
        """ Return a model query with the given filters.

        The query can be further customised like any ndb query.

        :return google.appengine.ext.ndb.Query:
            The query with the given filters already applied.
        """
        filters = [getattr(self.model, n) == v for n, v in iteritems(filters)]
        return self.get_queryset(request).filter(*filters).all()

    def get_requested(self, request):
        """ Get requested item. """
        pk = self.get_pk(request)
        return self.get_queryset(request).filter(
            self.model.id == pk
        ).one_or_none()

    def get_queryset(self, request):
        """ Extension point for one place to limit the data returned.

        Both .dbquery() and .get_requested() use this function as the base
        queryset. This means that if you need to restrict access to some db
        entries, you can just overload this method.

        :param request:
            The request associated with the call. Not used by default, but can
            be handy when overriding.
        :return:
            The SQLAlchemy resource.
        """
        return self.model.query
