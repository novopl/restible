# -*- coding: utf-8 -*-
"""
This is fabrics configuration file.
"""
from __future__ import absolute_import

# Configure the build
from peltak.core import conf
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
from peltak.commands import docs
from peltak.commands import git
from peltak.commands import lint
from peltak.commands import release
from peltak.commands import test
from peltak.commands import version
