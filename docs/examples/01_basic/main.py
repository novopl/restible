# -*- coding: utf-8 -*-
""" A very basic example of how to expose a model over HTTP as REST API. """
from __future__ import absolute_import, unicode_literals

# stdlib imports
from datetime import datetime

# 3rd party imports
import flask
import flask_sqlalchemy
import restible
import restible.util
import restible_flask
from sqlalchemy.exc import SQLAlchemyError


db = flask_sqlalchemy.SQLAlchemy()
DATETIME_FMT = '%Y-%d-%m %H:%M:%S'


def create_app():
    app = flask.Flask(__name__)
    app.config.update({
        'DEBUG': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///data.sqlite',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    with app.app_context():
        db.init_app(app)
        db.create_all()

        restible_flask.Endpoint.init_app(app, resources=[
            ['/api/post', BlogPostResource],
        ])

    return app


# Our application models
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at and self.created_at.strftime(DATETIME_FMT),
            'updated_at': self.updated_at and self.updated_at.strftime(DATETIME_FMT),
        }


# This is the REST resource associated for BlogPost. We're using
# `restible.RestResource` which comes with least amount of functionality
# built-in so everything has to be done manually. There are more base resource
# classes provided by restible and third party libraries. Here we just want to
# kick things of with the simplest one (rarely used in real applications).
class BlogPostResource(restible.RestResource):
    name = 'post'
    route_params = [{"name": "post_pk"}]

    def rest_query(self, request, params, payload):
        """ This is the GET /api/post route.

        This route will allow to get the list of all existing blog posts. In
        real app, this will probably also support some filtering of the results
        and possibly pagination as well.
        """
        posts = BlogPost.query.all()
        return 200, [x.serialize() for x in posts]

    def rest_get(self, request, params, payload):
        post_id = int(self.get_pk(request))
        item = BlogPost.query.filter(BlogPost.id == post_id).one_or_none()
        if item:
            return 200, item.serialize()
        else:
            return 404, {'detail': "Blog post #{} not found".format(post_id)}

    def rest_create(self, request, params, payload):
        session = BlogPost.query.session

        try:
            # Our basic validation only checks if all fields are present.
            missing = frozenset(['title', 'content']) - frozenset(payload.keys())
            if missing:
                raise restible.BadRequest("Missing fields: {}".format(missing))

            # Create a new BlogPost record and commit it to database.
            post = BlogPost(**payload)
            session.add(post)
            session.commit()

            return 201, post.serialize()

        except SQLAlchemyError as ex:
            session.rollback()
            return 500, {'detail': "DB ERROR: {}".format(ex)}

    def rest_update(self, request, params, payload):
        session = BlogPost.query.session
        post_id = int(self.get_pk(request))

        # Find the blog post we want to update.
        post = BlogPost.query.filter(BlogPost.id == post_id).one_or_none()
        if post is None:
            return 404, {'detail': "Blog post #{} not found".format(post_id)}

        # Make sure we do not overwrite read only fields.
        read_only = ['id', 'created_at', 'updated_at']
        for field in read_only:
            payload.pop(field, None)

        try:
            # Update the database record and commit.
            restible.util.update_from_values(post, payload)
            session.commit()

            return 200, post.serialize()

        except SQLAlchemyError as ex:
            session.rollback()
            return 500, {'detail': "DB ERROR: {}".format(ex)}

    def rest_delete(self, request, params, payload):
        session = BlogPost.query.session
        post_id = int(self.get_pk(request))

        try:
            BlogPost.query.filter(BlogPost.id == post_id).delete()
            session.commit()
            return 204, {'detail': "Blog post #{} deleted".format(post_id)}
        except SQLAlchemyError as ex:
            session.rollback()
            return 500, {'detail': "DB ERROR: {}".format(ex)}


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)

