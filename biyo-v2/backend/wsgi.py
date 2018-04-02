# -*- coding: utf-8 -*-
"""
WSGI config for pulsewallet project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/

See answers below regarding the trick implemented in this file.
http://stackoverflow.com/a/26981499/494631
http://stackoverflow.com/a/19759904/494631
http://stackoverflow.com/a/21124143/494631
"""

import os
import django
from django.core.handlers.wsgi import WSGIHandler
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")


class WSGIEnvironment(WSGIHandler):

    def __call__(self, environ, start_response):

        if 'DJANGO_SETTINGS_MODULE' in environ:
            os.environ['DJANGO_SETTINGS_MODULE'] = environ['DJANGO_SETTINGS_MODULE']
        django.setup()
        return super(WSGIEnvironment, self).__call__(environ, start_response)

application = WSGIEnvironment()
