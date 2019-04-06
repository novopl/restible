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

    rest_handlers = (
        res.rest_query,
        res.rest_query,
        res.rest_get,
        res.rest_create,
        res.rest_update,
        res.rest_delete,
        res.rest_options,
        res.rest_head,
    )

    for handler in rest_handlers:
        with pytest.raises(NotImplementedError):
            handler(request=None, params={}, payload={})
