# -*- coding: utf-8 -*-
#
# Requirements:
#   - Flask
#   - Flask-SQLAlchemy
#   - restible
#   - restible-flask
#   - restible-sqlalchemy
#   - serafin
#   - serafin-sqlalchemy
#
from __future__ import absolute_import, unicode_literals

# stdlib imports
from datetime import datetime

# 3rd party imports
import serafin_sqlalchemy       # pylint: disable=unused_import
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from restible_flask import FlaskEndpoint
from restible_sqlalchemy import SqlAlchemyResource

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


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)


# All rest XXX_item methods are already implemented in SqlAlchemyResource.
# You can disable any method by overriding it and raising NotImplementedError.
class BlogPostApi(SqlAlchemyResource):
    name = 'post'
    model = BlogPost

    def delete_item(self, request, params, payload):
        raise NotImplementedError("Cannot delete blog posts")


FlaskEndpoint.init_app(
    app,
    resources=[
        ['/api/posts', BlogPostApi, {'protected': False}],
    ]
)


db.create_all()
app.run(port=5000)
