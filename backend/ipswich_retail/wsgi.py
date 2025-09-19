"""
WSGI config for ipswich_retail project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ipswich_retail.settings')

application = get_wsgi_application()
