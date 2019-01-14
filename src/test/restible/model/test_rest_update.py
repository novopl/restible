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
    read_only = ['value']
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "value": {"type": "string"},
        },
        "additionalProperties": False,
    }


def test_uses_ModelResource_update_item():
    res = FakeRes()
    res.update_item = Mock(return_value={'name': 'instance1', 'value': 'hello'})

    req_data = {'name': 'fake1', 'value': 'fake'}
    result = res.rest_update(None, req_data)

    res.update_item.assert_called_once()

    assert result[0] == 200
    assert result[1] == {'name': 'instance1', 'value': 'hello'}


@pytest.mark.parametrize('req_data', [
    {'value': 'a'},
    {}
])
def test_allows_missing_values_even_if_they_are_required(req_data):
    """ We allow partial update - can be changed by overriding rest_update. """
    res = FakeRes()
    res.schema['required'] = ['name']
    res.update_item = Mock(return_value={'name': 'a', 'value': 'b'})

    result = res.rest_update(None, req_data)

    assert result[0] == 200


@pytest.mark.parametrize('req_data', [
    {'name': 'a', 'extra': 'a'},
    {'name': 1},
])
def test_returns_400_if_data_is_not_valid(req_data):
    res = FakeRes()
    res.update_item = Mock(return_value={'name': 'a', 'value': 'b'})

    result = res.rest_update(None, req_data)

    assert result[0] == 400
    assert 'detail' in result[1]


def test_returns_404_if_update_item_returns_None():
    res = FakeRes()
    res.update_item = Mock(return_value=None)

    result = res.rest_update(None, {})

    res.update_item.assert_called_once()

    assert result[0] == 404
    assert result[1]['detail'] == 'Not Found'


def test_returns_404_if_the_resource_does_not_implement_update_item():
    res = FakeRes()

    result = res.rest_update(None, {})

    assert result[0] == 404
    assert result[1]['detail'] == 'Not Found'
