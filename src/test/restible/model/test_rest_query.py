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


def test_uses_ModelResource_dbquery():
    res = FakeRes()
    res.dbquery = Mock(return_value=[
        {'name': 'instance1'},
        {'name': 'instance2'},
    ])

    result = res.rest_query(None, {})

    res.dbquery.assert_called_once()

    assert result[0] == 200
    assert result[1] == [
        {'name': 'instance1'},
        {'name': 'instance2'},
    ]


def test_returns_404_if_the_resource_does_not_implement_dbquery():
    res = FakeRes()

    req_data = {'name': 'fake request data'}
    result = res.rest_query(None, req_data)

    assert result[0] == 404
    assert result[1]['detail'] == 'Not Found'
