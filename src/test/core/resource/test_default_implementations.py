# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# 3rd party imports
import pytest

# Project imports
from restible import RestResource


def test_default_implementation_raises_NotImplemented():
    class FakeResource(RestResource):
        name = 'fake'

    res = FakeResource()

    # Somehow using @parametrize and getattr will not be picked up by coverage.
    test_params = (
        (res.rest_query, dict(filters={})),
        (res.rest_query, dict(filters={})),
        (res.rest_get, dict()),
        (res.rest_create, dict(data={})),
        (res.rest_update, dict(data={})),
        (res.rest_delete, dict()),
        (res.rest_options, dict()),
        (res.rest_head, dict()),
    )

    for handler, args in test_params:
        with pytest.raises(NotImplementedError):
            handler(request=None, **args)
