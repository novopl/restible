# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# stdlib imports
import sys
from os.path import dirname, relpath


# django-1.11 doesn't support python 3.3
if sys.version_info[:2] == (3, 3):
    collect_ignore = ['django']


def pytest_itemcollected(item):
    """ Prettier test names. """
    name = item.originalname or item.name
    if name.startswith('test_'):
        name = name[5:]

    name = name.replace('_', ' ').strip()
    name = name[0].upper() + name[1:]

    rel_path = relpath(item.fspath.strpath, dirname(item.fspath.dirname))
    item._nodeid = '{location:50} {name}'.format(
        name=name,
        location='{}:{}'.format(rel_path, item.location[1]),
    )
