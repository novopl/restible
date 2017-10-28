# -*- coding: utf-8 -*-
"""
Test settings for django integration
"""
from __future__ import absolute_import, unicode_literals


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '07s#p@ol!&7$et@@yh=q^r42qr74pjes!sosahjszt#g1yaqyz'
SITE_ID = 1

DEBUG = False
ALLOWED_HOSTS = []


STATIC_URL = '/static/'
STATIC_ROOT = 'static'
# devserver will only serve static files from the first directory below.
STATICFILES_DIRS = []
ROOT_URLCONF = 'fake.urls'

INSTALLED_APPS = (
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
