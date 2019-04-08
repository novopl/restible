# -*- coding: utf-8 -*-
"""
 This is a very basic example of how to expose a model over HTTP as REST API.
 The example below is geared toward using the least amount of code to achieve
 it's goals. For this example we're using *restible* with *Flask* and
 *SQLAlchemy* since it's easy to set up, allows for self-contained easy to
 follow code and simple code. You can also use other underlying frameworks
 through other integrations like **restible-django** or **restible-appengine**.

 Requirements:
   - Flask
   - Flask-SQLAlchemy
   - restible
   - restible-flask
   - restible-sqlalchemy
   - serafin
   - serafin-sqlalchemy

"""

from __future__ import absolute_import, unicode_literals

# stdlib imports
from datetime import datetime

# 3rd party imports
import restible.util
import serafin_sqlalchemy       # pylint: disable=unused_import
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from restible_flask import FlaskEndpoint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


# Initialise the flask WSGI application.
app = Flask(__name__)
app.config.update({
    'DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///data.sqlite',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
})

db = SQLAlchemy(app)

# Create serializer for our base model class. Store it in the variable so it's
# not garbage collected. This function will be used by ``serafin.serialize()``
# function to serialize SQLAlchemy models.
model_serializer = serafin_sqlalchemy.make_serializer(db.Model)


# Our application models
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)


# SqlAlchemyResource will implement all basic REST CRUD methods. If you
# need to disable a route, you can do
class BlogPostApi(restible.ModelResource):
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

    def create_item(self, request, params, payload):
        try:
            item = self.model(**payload)

            self.session.add(item)
            self.session.commit()

            return item
        except IntegrityError:
            self.session.rollback()
            raise restible.ModelResource.AlreadyExists()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise restible.Error("DB ERROR: {}".format(ex))

    def query_items(self, request, params, payload):
        return [x.serialize() for x in BlogPost.query.all()]

    def get_item(self, request, params, payload):
        return self.item_for_request(request)

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


FlaskEndpoint.init_app(
    app,
    resources=[
        ['/api/posts', BlogPostApi, {'protected': False}],
    ]
)


db.create_all()
app.run(port=5000)
