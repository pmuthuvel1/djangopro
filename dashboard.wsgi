import os
import sys
import site

sys.path.append('/opt/www/dashboard')
sys.path.append('/opt/www/dashboard/dashboard')

execfile(activate_env, dict(__file__=activate_env))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dashboard.settings")

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

