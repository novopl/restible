# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# local imports
from restible import RestResource


class FakeResource(RestResource):
    name = 'fake'


class FakeRequest(object):
    def __init__(self, rest_keys):
        self.rest_keys = rest_keys


def test_returns_the_key_if_present():
    request = FakeRequest(rest_keys={
        'fake_pk': 1
    })

    pk = FakeResource().get_pk(request)

    assert pk == 1


def test_returns_None_if_pk_is_missing():
    request = FakeRequest(rest_keys={})

    pk = FakeResource().get_pk(request)

    assert pk is None


def test_returns_None_if_request_does_not_have_rest_keys():
    request = {}

    pk = FakeResource().get_pk(request)

    assert pk is None
