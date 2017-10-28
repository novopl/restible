# -*- coding: utf-8 -*-
"""
Git helpers.
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
from os.path import dirname

# 3rd party imports
from fabric.api import lcd, local, quiet


def current_branch():
    """ Return the name of the currently checked out git branch. """
    with quiet():
        return local('git symbolic-ref --short HEAD', capture=True).stdout


def is_dirty():
    """ Return **True** if there are any changes/unstaged files. """
    cmd_dir = dirname(__file__)
    with lcd(cmd_dir):
        with quiet():
            status = local('git status --porcelain', capture=True).stdout
            return bool(status.strip())
