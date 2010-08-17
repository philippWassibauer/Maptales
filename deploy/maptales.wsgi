import os
import sys

sys.stdout = sys.stderr

from os.path import abspath, dirname, join
from site import addsitedir

sys.path.insert(0, abspath(join(dirname(__file__), "../../")))

from django.conf import settings
os.environ["DJANGO_SETTINGS_MODULE"] = "maptales.settings"

sys.path.insert(0, join(settings.PINAX_ROOT, "apps"))
sys.path.insert(0, join(settings.PROJECT_ROOT, "apps"))
sys.path.insert(0, "/home/pinax-0.7.1/lib/python2.5/site-packages/")

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()












