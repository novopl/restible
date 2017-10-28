# -*- coding: utf-8 -*-
"""
Integration with django.

All django dependant code should live in this package. Everything else
should not depend on django in any way.
"""
from __future__ import absolute_import, unicode_literals
from .endpoint import DjangoEndpoint
