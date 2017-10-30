# -*- coding: utf-8 -*-
"""
Functionality related to filters.

Filters are used by when querying the resource. For now the functionality is
quite simple - we just extract the filters from GET query params.
"""
from __future__ import absolute_import, unicode_literals


def extract(get_params):
    """ Extract filters from request GET params.

    :param HttpRequest request:
    :return dict:
    """
    filters = {}
    for name, value in get_params.items():
        filters[name] = from_string(value)

    return filters


def from_string(value):
    """ Convert the given string value to the actual type it holds.

    If the string is an integer it will return an int, if it's a float, then it
    will return float otherwise it will just return a string.

    TODO: Add date and datetime support
    """
    try:
        if value.isdigit():
            return int(value)
        else:
            return float(value)
    except ValueError:
        return value
