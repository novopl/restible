# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# 3rd party imports
import pytest
from six import string_types

# project imports
from restible.url_params import from_string


@pytest.mark.parametrize('value,expected_type', (
    ('123', int),
    ('3.14159', float),
    ('value', string_types),
))
def test_coerces_to_the_right_type(value, expected_type):
    result = from_string(value)

    assert isinstance(result, expected_type)
