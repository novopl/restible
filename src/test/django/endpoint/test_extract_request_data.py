# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# 3rd party imports
import pytest

# local imports
from restible.integrations.django import DjangoEndpoint


class FakeRequest(object):
    def __init__(self, **kwargs):
        self.body = kwargs.pop('body', '').encode('utf-8')
        self.GET = kwargs.pop('query', {})

        for name, value in kwargs.items():
            setattr(self, name, value)


def test_raises_ValueError_on_invalid_json():
    request = FakeRequest(content_type='application/json', body='fake_data')

    with pytest.raises(ValueError):
        DjangoEndpoint.extract_request_data(request)
