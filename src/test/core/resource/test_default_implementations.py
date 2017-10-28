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
        (res.query, dict(filters={})),
        (res.query, dict(filters={})),
        (res.get, dict()),
        (res.create, dict(data={})),
        (res.update, dict(data={})),
        (res.delete, dict()),
        (res.options, dict()),
        (res.head, dict()),
    )

    for handler, args in test_params:
        with pytest.raises(NotImplementedError):
            handler(request=None, **args)
