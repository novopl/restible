# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# 3rd party imports
import pytest

# Project imports
from restible import RestEndpoint


class InvalidFakeResource(object):
    pass


@pytest.mark.parametrize('resource', (
    None,                   # Not given
    InvalidFakeResource,  # Not a RestResource subclass
    10,                     # Not a RestResource subclass
    'some_string'           # Not a RestResource subclass
))
def test_raises_ValueError_if_resource_is_not_a_valid_resource(resource):
    with pytest.raises(ValueError):
        RestEndpoint(resource)
