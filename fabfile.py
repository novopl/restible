# -*- coding: utf-8 -*-
"""
This is fabrics configuration file.
"""
from __future__ import absolute_import

# Configure the build
from ops.commands.common import conf
conf.init({
    'SRC_DIR': 'src',
    'SRC_PATH': 'src/restible',
    'BUILD_DIR': '.build',
    'DJANGO_TEST_SETTINGS': 'test.django.settings',
    'PKGS_PATHS': [
        'src/restible',
        'src/test',
        'ops/commands',
    ],
    'TEST_TYPES': {
        'default': {'paths': [
            'src/test',
            'ops/commands',
        ]}
    }
})

# Import all commands
from ops.commands.clean import *
from ops.commands.docs import *
from ops.commands.git import *
from ops.commands.lint import *
from ops.commands.ops import *
from ops.commands.release import *
from ops.commands.test import *
