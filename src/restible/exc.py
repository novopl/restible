# -*- coding: utf-8 -*-
""" Exception classes for restible. """
from __future__ import absolute_import, unicode_literals


class Error(Exception):
    """ Base exception class for restible related errors. """
    status = 500
    detail = "Unknown Error"

    def __init__(self, detail=None, status=None):
        super(Error, self).__init__(detail)
        self.detail = detail or self.detail
        self.status = status or self.status


class BadRequest(Error):
    """ Will be converted to HTTP 400 Bad Request. """
    status = 400
    detail = "Bad Request"


class NotAuthorized(Error):
    """ Will be converted to HTTP 401 Not Authorized. """
    status = 401
    detail = "Not Authorized"


class NotAllowed(Error):
    """ Will be converted to HTTP 403 Not Allowed. """
    status = 403
    detail = "Not Allowed"


class NotFound(Error):
    """ Will be converted to HTTP 404 Not Found. """
    status = 404
    detail = "Not Found"
