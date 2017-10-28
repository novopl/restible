# -*- coding: utf-8 -*-
"""
Core REST API code.

This package exists so we can separate the REST API MVP from the rest of the
code. The code that lives in this package should not require anything else to
run and should also provide a minimal set of tools for building an API.

All advanced functionality should be implemented in other packages.
"""
from __future__ import absolute_import, unicode_literals
