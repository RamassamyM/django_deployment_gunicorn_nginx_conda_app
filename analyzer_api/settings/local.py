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

INSTALLED_APPS += [
        'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INTERNAL_IPS = ['127.0.0.1', '.localhost', '192.168.0.217']

DEBUG_TOOLBAR_PANELS = [
       'debug_toolbar.panels.versions.VersionsPanel',
       'debug_toolbar.panels.timer.TimerPanel',
       'debug_toolbar.panels.settings.SettingsPanel',
       'debug_toolbar.panels.headers.HeadersPanel',
       'debug_toolbar.panels.request.RequestPanel',
       'debug_toolbar.panels.sql.SQLPanel',
       'debug_toolbar.panels.staticfiles.StaticFilesPanel',
       'debug_toolbar.panels.templates.TemplatesPanel',
       'debug_toolbar.panels.cache.CachePanel',
       'debug_toolbar.panels.signals.SignalsPanel',
       'debug_toolbar.panels.logging.LoggingPanel',
       'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
        'JQUERY_URL': '',
        'INTERCEPT_REDIRECTS': False,
 }

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
