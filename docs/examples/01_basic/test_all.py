# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import pytest
from main import db, create_app, BlogPost
from flask.testing import FlaskClient


@pytest.fixture()
def client():
    app = create_app()

    with app.app_context():
        yield app.test_client()
        db.drop_all()


def test_can_query_posts(client):
    # type: (FlaskClient) -> None
    # Setup
    _commit(
        BlogPost(title='Post 1', content='Post 1 content'),
        BlogPost(title='Post 2', content='Post 2 content'),
    )

    # Test
    r = client.get('/api/post')
    assert r.status_code == 200
    assert len(r.json) == 2
    assert frozenset(('Post 1', 'Post 2')) == frozenset(x['title'] for x in r.json)


def test_can_get_post(client):
    # type: (FlaskClient) -> None
    post = BlogPost(title='Post 1', content='Post 1 content')
    _commit(post)

    r = client.get('/api/post/{}'.format(post.id))

    assert r.json['id'] == post.id
    assert r.json['title'] == post.title
    assert r.json['content'] == post.content


def test_can_create_post(client):
    # type: (FlaskClient) -> None
    r = client.post(
        '/api/post',
        content_type='application/json',
        data=json.dumps({
            "title": "My blog post",
            "content": "This is my blog post content."
        })
    )

    assert r.status_code == 201, r.data.decode('utf-8')

    post = BlogPost.query.filter(BlogPost.id == r.json['id']).one_or_none()

    assert post is not None
    assert post.title == 'My blog post'
    assert post.content == 'This is my blog post content.'


def test_can_update_post(client):
    # type: (FlaskClient) -> None
    post, = _commit(BlogPost(title='Post 1', content='Post 1 content'))

    r = client.put(
        '/api/post/{}'.format(post.id),
        content_type='application/json',
        data=json.dumps({
            "title": "title",
            "content": "content"
        })
    )

    assert r.status_code == 200, r.data.decode('utf-8')

    BlogPost.query.session.refresh(post)
    assert post.title == 'title'
    assert post.content == 'content'


def test_can_delete_post(client):
    # type: (FlaskClient) -> None
    # Setup
    post1, post2 = _commit(
        BlogPost(title='Post 1', content='Post 1 content'),
        BlogPost(title='Post 2', content='Post 2 content')
    )

    r = client.delete('/api/post/{}'.format(post1.id))

    assert r.status_code == 204, r.data.decode('utf-8')

    posts = BlogPost.query.all()

    assert len(posts) == 1
    assert posts[0].title == post2.title


def _commit(*items):
    if not items:
        return

    session = items[0].__class__.query.session
    session.add_all(items)
    session.commit()
    return items
