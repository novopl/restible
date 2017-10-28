# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# 3rd party imports
import pytest

# Project imports
from restible import RestEndpoint


@pytest.mark.parametrize('http_method,pk,expected_result', (
    ('POST', None, 'create'),
    ('POST', 1234, None),
    ('GET', None, 'query'),
    ('GET', 1234, 'get'),
    ('PUT', None, None),
    ('PUT', 1234, 'update'),
    ('DELETE', None, None),
    ('DELETE', 1234, 'delete'),
    ('HEAD', None, 'head'),
    ('HEAD', 1234, 'head'),
    ('OPTIONS', None, 'options'),
    ('OPTIONS', 1234, 'options'),
))
def test_correctly_resolves_method_and_pk(http_method, pk, expected_result):
    verb = RestEndpoint.determine_rest_verb(http_method, pk)

    assert verb == expected_result
