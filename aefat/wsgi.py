from django.core.wsgi import get_wsgi_application
import os

from dj_static import Cling


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aefat.settings")


application = Cling(get_wsgi_application())
