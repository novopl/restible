# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# 3rd party imports
import pytest

# local imports
from restible import util


class User(object):
    def __init__(self, name='John', age=35, admin=False):
        self.name = name
        self.age = age
        self.admin = admin


class StaticUser(object):
    __slots__ = ['name', 'age', 'admin']

    def __init__(self, name='John', age=35, admin=False):
        self.name = name
        self.age = age
        self.admin = admin


def test_updates_attributes_correctly():
    user = User()

    util.update_from_values(user, {
        'name': 'Dave',
        'age': 20,
        'admin': True
    })

    assert user.name == 'Dave'
    assert user.age == 20
    assert user.admin is True


def test_supports_partial_updates():
    user = User()

    util.update_from_values(user, {'admin': True})

    assert user.name == 'John'
    assert user.age == 35
    assert user.admin is True


def test_will_add_new_attribute_if_it_doesnt_exist():
    user = User()

    util.update_from_values(user, {'new_attr': 'hello'})

    assert user.new_attr == 'hello'


def test_raises_AttributeError_if_cant_set_attribute():
    user = StaticUser()

    with pytest.raises(AttributeError):
        util.update_from_values(user, {'new_attr': 'hello'})
