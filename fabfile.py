# -*- coding: utf-8 -*-
"""
This is fabrics configuration file.
"""
from __future__ import absolute_import

# Configure the build
from fabops.commands.common import conf
conf.init({
    'SRC_DIR': 'src',
    'SRC_PATH': 'src/restible',
    'BUILD_DIR': '.build',
    'DJANGO_TEST_SETTINGS': 'test.django.settings',
    'DOC_SRC_PATHS': 'docs',
    'LINT_PATHS': [
        'src/restible',
        'src/test',
    ],
    'CLEAN_PATTERNS': [
        '__pycache__',
        '*.py[cod]',
        '.swp',
        '.cache',
        '.build'
    ],
    'REFDOC_PATHS': [
        'src/restible',
    ],
    'TEST_TYPES': {
        'default': {'paths': ['src/test']},
        'no_django': {
            'mark': 'not django',
            'paths': [
                'src/test',
            ]
        }
    }
})

# Import all commands
from fabops.commands.clean import *
from fabops.commands.docs import *
from fabops.commands.git import *
from fabops.commands.lint import *
from fabops.commands.ops import *
from fabops.commands.release import *
from fabops.commands.test import *
