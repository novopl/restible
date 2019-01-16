# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# 3rd party imports
from mock import Mock

# local imports
from restible import ModelResource


class FakeRes(ModelResource):
    name = 'fake_res'
    schema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
            }
        },
        "required": ["name"],
        "additionalProperties": False
    }


def test_uses_ModelResource_get_requested():
    res = FakeRes()
    res.get_item = Mock(return_value={'name': 'instance'})

    result = res.rest_get(None, {})

    res.get_item.assert_called_once()

    assert result[0] == 200
    assert result[1] == {'name': 'instance'}


def test_returns_404_if_get_requested_returns_None():
    res = FakeRes()
    res.get_item = Mock(return_value=None)

    result = res.rest_get(None, {})

    res.get_item.assert_called_once()

    assert result[0] == 404
    assert result[1]['detail'] == 'Not Found'


def test_returns_404_if_the_resource_does_not_implement_get_requested():
    res = FakeRes()

    result = res.rest_get(None, {})

    assert result[0] == 404
    assert result[1]['detail'] == 'Not Found'
