from base import *


DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3'
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)


DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
}

env_config_file = '../env_configuration/ci_config.json'


import os
import json
from django.core.exceptions import ImproperlyConfigured

with open(os.environ.get(env_config_file)) as f:
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

ALLOWED_HOSTS = [SECRET_ALLOWED_HOST,]
