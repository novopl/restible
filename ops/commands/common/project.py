# -*- coding: utf-8 -*-
"""
Project related helpers.
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
from contextlib import contextmanager
from os.path import dirname, join, normpath

# 3rd party imports
from fabric.api import lcd, quiet as fabric_quiet


def _repo_path(path):
    """ Return absolute path to the repo dir (root project directory). """
    return normpath(join(dirname(__file__), '../../..', path))


@contextmanager
def inside(path='.', quiet=False):
    """ Return absolute path to the repo dir (root project directory). """
    with lcd(_repo_path(path)):
        if quiet:
            with fabric_quiet():
                yield
        else:
            yield
