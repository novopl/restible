# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# 3rd party imports
import pytest

# Project imports
from restible import RestEndpoint, RestResource


class FakeResource(RestResource):
    name = 'fake'


@pytest.mark.parametrize('method_name,args', (
    ('extract_request_data', {'request': None}),
))
def test_abstract_methods_raise_NotImplementedError(method_name, args):
    endpoint = RestEndpoint(res_cls=FakeResource)

    with pytest.raises(NotImplementedError):
        method = getattr(endpoint, method_name)

        method(**args)
