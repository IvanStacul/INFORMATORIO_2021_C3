import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhitenoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chacu_py.settings.production')

application = get_wsgi_application()
application = DjangoWhitenoise(application)
