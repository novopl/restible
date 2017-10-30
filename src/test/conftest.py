# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# stdlib imports
import sys


# django-1.11 doesn't support python 3.3
if sys.version_info[:2] == (3, 3):
    collect_ignore = ['django']

