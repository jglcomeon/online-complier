"""
WSGI config for myweb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys
sys.path.append('/Users/jgl/Desktop/save_envir1/h2/lib/python3.6/site-packages')
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myweb.settings")

application = get_wsgi_application()
