# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# 3rd party imports
import pytest

# Project imports
from restible.core.filters import extract


@pytest.mark.parametrize('data', (
    ({'filter': 'value'}),
    ({'filter': 123}),
    ({'filter': 3.14159}),
    ({
        'filter1': 'value1',
        'filter2': 123,
        'filter3': 3.14159
    })
))
def test_extracts_values_correctly(data, rf):
    request = rf.get('/', data)

    filters = extract(request)

    assert filters == data


@pytest.mark.parametrize('params,expected', (
    ('filter=value', {'filter': 'value'}),
    ('filter=123', {'filter': 123}),
    ('filter=3.14159', {'filter': 3.14159}),
    ('filter1=value&filter2=123&filter3=3.14159', {
        'filter1': 'value',
        'filter2': 123,
        'filter3': 3.14159
    })
))
def test_extracts_values_correctly_when_passing_pure_url(params, expected, rf):
    request = rf.get('/?' + params)

    filters = extract(request)

    assert filters == expected


def test_duplicate_filters_raise_ValueError(rf):
    request = rf.get('/?value=first&value=second')

    with pytest.raises(ValueError):
        extract(request)
