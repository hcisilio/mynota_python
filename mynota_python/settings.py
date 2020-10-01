 # -*- coding: utf-8 -*-
try:
    from .settings_base import *
except ImportError as e:
    pass

#Heroku-configs
import django_heroku
# Activate Django-Heroku.
django_heroku.settings(locals())
