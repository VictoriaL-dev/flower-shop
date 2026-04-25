"""
WSGI config for flower_shop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_shop.settings')

import flower_shop.logger  # production entry point — logging is also configured in manage.py for dev

application = get_wsgi_application()
