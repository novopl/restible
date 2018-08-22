# -*- coding: utf-8 -*-
"""

Integration with webapp2.

All webapp2 dependant code should live in this package. webapp2 is the default
framework used by Google AppEngine so it makes restible based apps easy to
implement for this platform.
"""
from __future__ import absolute_import, unicode_literals
from .endpoint import Webapp2Endpoint
