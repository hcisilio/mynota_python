 # -*- coding: utf-8 -*-
try:
    from .settings_base import *
except ImportError as e:
    pass

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
#Heroku-configs
import django_heroku
# Activate Django-Heroku.
django_heroku.settings(locals())
