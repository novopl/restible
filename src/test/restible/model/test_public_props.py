# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# 3rd party imports
from mock import patch, Mock

# local imports
from restible import ModelResource


class FakeModel(object):
    @property
    def prop1(self):
        return 1

    @property
    def prop2(self):
        return 2


class FakeRes(ModelResource):
    name = 'fake_res'
    model = FakeModel


@patch('restible.model.iter_public_props')
def test_iter_public_props_called_only_once(p_iter_public_props):
    # type: (Mock) -> None
    res = FakeRes()

    _ = res.public_props
    _ = res.public_props

    p_iter_public_props.assert_called_once()


def test_returns_all_properties():
    # type: (Mock) -> None
    res = FakeRes()

    assert len(res.public_props) == 2
    assert set(res.public_props) == {'prop1', 'prop2'}


# Used only in type hint comments. Will be removed together with py2 support
del Mock
