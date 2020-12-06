"""
WSGI config for dfa project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys, site

from django.core.wsgi import get_wsgi_application
from os.path import dirname, abspath, join

site.addsitedir('/home/felixw/digifaa/env/lib/python3.7/site-packages')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dfa.settings')

application = get_wsgi_application()
