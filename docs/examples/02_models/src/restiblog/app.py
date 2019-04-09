# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# 3rd party imports
import flask
import flask_sqlalchemy


app = None
db = flask_sqlalchemy.SQLAlchemy()
DATETIME_FMT = '%Y-%d-%m %H:%M:%S'


def create_app():
    global app
    app = flask.Flask(__name__)
    app.config.update({
        'DEBUG': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///data.sqlite',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    with app.app_context():
        init_db(app)

        from .routes import init_routes
        init_routes(app)


def init_db(app):
    db.init_app(app)
    db.create_all()


def run_devserver(**opts):
    opts.setdefault('port', 5000)

    app = create_app()
    app.run(**opts)
