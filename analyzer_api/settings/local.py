# create a directory /env_configuration/ and add different config files :
# ci_config.json, local_config.json, production_config.json, staging_config.json, testing_config.json
# like this one for production for example :
# {
#     "SECRET_KEY" : "mykey",
#     "DATABASE_URL" : "postgres://user:michael@localhost:5432/xxxxxxxxxxx",
#     "EMAIL_HOST_USER" : "user",
#     "EMAIL_HOST_PASSWORD" : "password",
#     "SECRET_ALLOWED_HOST" : "['.localhost', '127.0.0.1:8000', '127.0.0.1']"
# }


from ..settings.base import *

DEBUG = True

# INSTALLED_APPS += [
#     'debug_toolbar',
# ]
#
# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# DEBUG_TOOLBAR_CONFIG = {
#     'JQUERY_URL': '',
# }

env_config_file = BASE_DIR + '/env_configuration/local_config.json'


import os
import json
from django.core.exceptions import ImproperlyConfigured

with open(env_config_file) as f:
 configs = json.loads(f.read())

def get_env_var(setting, configs=configs):
 try:
     val = configs[setting]
     if val == 'True':
         val = True
     elif val == 'False':
         val = False
     return val
 except KeyError:
     error_msg = "ImproperlyConfigured: Set {0} environment      variable".format(setting)
     raise ImproperlyConfigured(error_msg)
#get secret key
SECRET_KEY = get_env_var("SECRET_KEY")

ALLOWED_HOSTS = ['.localhost', '127.0.0.1']
