# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# 3rd party imports
import pytest
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


def test_uses_ModelResource_create_item():
    res = FakeRes()
    res.create_item = Mock(return_value={'fake': 'instance'})

    req_data = {'name': 'fake request data'}
    data = res.rest_create(None, req_data)

    res.create_item.assert_called_once()
    assert data == {'fake': 'instance'}


@pytest.mark.parametrize('req_data', [
    {'name': 'fake request data', 'extra': 'invalid'},
    {'missing': 'required field'},
    {'name': 1},
])
def test_returns_400_if_data_is_not_valid(req_data):
    res = FakeRes()
    res.create_item = Mock(return_value={'fake': 'instance'})

    result = res.rest_create(None, req_data)

    assert result[0] == 400
    assert 'detail' in result[1]


def test_returns_400_if_instance_already_exists():
    res = FakeRes()
    res.create_item = Mock(side_effect=ModelResource.AlreadyExists)

    req_data = {'name': 'fake request data'}
    result = res.rest_create(None, req_data)

    assert result[0] == 400
    assert result[1]['detail'] == 'Already exists'


def test_returns_404_if_the_resource_does_not_implement_create_item():
    res = FakeRes()

    req_data = {'name': 'fake request data'}
    result = res.rest_create(None, req_data)

    assert result[0] == 404
    assert result[1]['detail'] == 'Not Found'
