# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# stdlib imports
from datetime import datetime

# 3rd party imports
import restible
import restible.util
import restible_flask
from sqlalchemy.exc import SQLAlchemyError

# local imports
from .models import BlogPost
from .app import DATETIME_FMT


def init_routes(app):
    restible_flask.Endpoint.init_app(app, resources=[
        ['/api/post', BlogPostResource],
    ])


class BlogPostResource(restible.ModelResource):
    name = 'post'
    model = BlogPost
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "title": {"type": "string"},
            "content": {"type": "string"},
            "created_at": {"type": "string"},
            "updated_at": {"type": "string"}
        }
    }

    @property
    def session(self):
        return self.model.query.session

    def deserialize(self, data):
        rv = dict(data)

        if 'created_at' in rv:
            rv['created_at'] = datetime.strptime(DATETIME_FMT)
        if 'updated_at' in rv:
            rv['updated_at'] = datetime.strptime(DATETIME_FMT)

        return rv

    def serialize(self, item_or_items, *args, **kw):
        try:
            return [x.serialize() for x in item_or_items]
        except:
            return item_or_items.serialize()

    def query_items(self, request, params, payload):
        return [x.serialize() for x in BlogPost.query.all()]

    def get_item(self, request, params, payload):
        return self.item_for_request(request)

    def create_item(self, request, params, payload):
        try:
            item = self.model(**payload)

            self.session.add(item)
            self.session.commit()

            return item
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise restible.Error("DB ERROR: {}".format(ex))

    def update_item(self, request, params, payload):
        item = self.item_for_request(request)
        if item is None:
            return None

        payload.pop('id', None)
        restible.util.update_from_values(item, payload)

        try:
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise restible.Error("DB ERROR: {}".format(ex))

        return item

    def delete_item(self, request, params, payload):
        pk = int(self.get_pk(request))
        try:
            BlogPost.query.filter(BlogPost.id == pk).delete()
            self.session.commit()

        except SQLAlchemyError as ex:
            self.session.rollback()
            raise restible.Error("DB ERROR: {}".format(ex))
