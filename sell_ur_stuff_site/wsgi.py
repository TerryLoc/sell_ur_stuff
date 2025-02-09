import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sell_ur_stuff_site.settings")

application = get_wsgi_application()
