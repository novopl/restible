# -*- coding: utf-8 -*-
"""
Helpers for setting up mapping between URLs and resources.
"""
from __future__ import absolute_import, unicode_literals
from .. import RestResource


def make_urls(default_endpoint_cls, endpoints):
    """

    :param list<RestEndpoint> endpoints:
    :return list<url>:

    """
    urls = []

    for endpoint in endpoints:
        if isinstance(endpoint, type) and issubclass(endpoint, RestResource):
            urls += default_endpoint_cls(endpoint).urls
        else:
            urls += endpoint.urls

    return urls
