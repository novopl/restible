# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# local imports
from restible import RestResource


class FakeResource(RestResource):
    name = 'fake'


def test_returns_the_key_if_present(rf):
    request = rf.get('/fake')
    request.rest_keys = {
        'fake_pk': 1
    }

    pk = FakeResource().get_my_pk(request)

    assert pk == 1


def test_returns_None_if_pk_is_missing(rf):
    request = rf.get('/fake')
    request.rest_keys = {}

    pk = FakeResource().get_my_pk(request)

    assert pk is None


def test_returns_None_if_request_does_not_have_rest_keys(rf):
    request = rf.get('/fake')

    pk = FakeResource().get_my_pk(request)

    assert pk is None
