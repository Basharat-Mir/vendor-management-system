import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vendor_management.settings')
settings.configure()
