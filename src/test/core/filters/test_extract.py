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
def test_extracts_values_correctly(data):
    filters = extract({str(n): str(v) for n, v in data.items()})

    assert filters == data
