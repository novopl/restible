# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# 3rd party imports
import pytest

# Project imports
from restible import RestResource


class InvalidFakeResource(object):
    pass


class FakeResource(RestResource):
    pass


@pytest.mark.parametrize('res_name', (
    None,               # Has to be given
    '',                 # Can't be empty
    'invalid name',     # No space allowed
    'invalid.name',     # No dots allowed
    '0invalid_name',    # Can't start with a digit
    'invalid-name',     # Can't contain a dash
    'invalid@name',     # Can't contain symbols
    'invalid$name',     # Can't contain symbols
    'invalid#name',     # Can't contain symbols
    'invalid^name',     # Can't contain symbols
))
def test_invalid_endpoint_name_raises_ValueError(res_name):
    with pytest.raises(ValueError):
        class FakeResource(RestResource):
            name = res_name

        FakeResource()


@pytest.mark.parametrize('res_name', (
    'valid_name',
    'Valid_name',
    '_valid_name',
    '_valid__name',
    'valid_123',
))
def test_valid_names_are_accepted(res_name):
    class FakeResource(RestResource):
        name = res_name

    FakeResource()
