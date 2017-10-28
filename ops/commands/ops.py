# -*- coding: utf-8 -*-
"""
Commands related directly to fabops.
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
import os.path

# 3rd party imports
from fabric.api import lcd, local

# local imports
from .common import git
from .common import log


def ops_update():
    """ Pull fabops-commands mainstream updates and merge with local. """
    commands_path = os.path.dirname(__file__)

    with lcd(commands_path):
        if git.is_dirty():
            log.err("commands repo is dirty, aborting.")
            return

        branch = git.current_branch()

        log.info("Checking out ^33master")
        local('git checkout master')

        log.info("Pulling latest changes")
        local('git pull origin master')

        log.info("Checking out ^33".format(branch))
        local('git checkout {}'.format(branch))

        log.info("Merging mainstream changes into ^33".format(branch))
        local('git merge master --no-edit')

        log.info("Done")
