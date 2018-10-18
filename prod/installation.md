# Déploiement app django sur serveur de prod :
###### Méthode  : systemd/nginx/miniconda/gunicorn/python/django/
Pré-requis : serveur linux avec accès root ou accès ssh

=> Read <http://docs.gunicorn.org/en/latest/deploy.html>
NB : protocole WSGI = spécification qui permet à un serveur web et une application Python de communiquer ensemble et ainsi récupérer les pages web générées par Django.

## SUR l'APPLICATION

### 1. Configurer le projet dans settings.py  de l'application django:

DEBUG = False

ALLOWED_HOSTS = ['adresseIP',]
ALLOWED_HOSTS = ['www.crepes-bretonnes.com', '.super-crepes.fr']. Le point au début du deuxième élément de la liste permet d'indiquer que tous les sous-domaines sont acceptés, autrement dit, les domaines suivants seront accessibles :super-crepes.fr, www.super-crepes.fr, mobile.super-crepes.fr

SECRET_KEY : générer une nouvelle clé avec ces commandes python par ex

```python
import random
import string
import secrets
key = ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&\*(-\_=+)') for i in range(50))
print(key)
```

ADMINS : valeur par défaut : [] (liste vide)
Une liste de toutes les personnes qui reçoivent les notifications d’erreurs dans le code. Lorsque DEBUG=False et que AdminEmailHandler est configuré dans LOGGING (comportement par défaut), Django envoie un courriel à ces personnes contenant les détails des exceptions produites dans le cycle requête/réponse.
Chaque élément de la liste doit être un tuple au format «(nom complet, adresse électronique)». Exemple
[('John', 'john@example.com'), ('Mary', 'mary@example.com')]

**Commandes** : lancer alors manage.py comme suit pour changer d'environnement :
python manage.py runserver --settings=mysite.settings.development
or
python manage.py migrate –settings=mysite.settings.production


Notes sur le code Django à modifier pour une meilleur config de prod :
***

SECURITE : changer dans manage.py :os.environ.setdefault('DJANGO_SETTINGS_MODULE', "mysite.settings.production")
pour éviter que ce soit la version de dev qui soit par défaut (en cas d’oubli en prod, on aura alors la mauvaise config : pb de sécurité)

Pour ne pas inscrire la secret_key sur git et différencier ses environnements (ci, local, staging, test, production) :

1. Créer à la place du fichier settings, un dossier settings avec les fichiers :
base.py ; ci.py ; local.py ; production.py ; staging.py ; testing.py et __init__.py

2. Dans base.py : reprendre settings.py sauf ce qu’on différencie dans local.py, production.py…

3. ex : dans local.py (commenter éventuellement les lignes contenant debug toolbar):

```Python
from ..settings.base import *

DEBUG = True
INSTALLED_APPS += [
    'debug_toolbar',
]
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
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

ALLOWED_HOSTS = ['.localhost', '127.0.0.1'. ]

```

On importe donc base
puis on rajoute les variables de conf nécessaires :
DEBUG = True par exemple…
on recherche les variables secrètes dans un fichier à créer.

CREER UN DOSSIER env_configuration au même niveau que settings/
et y ajouter les fichiers de configuration au format JSON :

ex : local_config.json
```JSON
{
  "SECRET_KEY" : "blablabla",
  "DATABASE_URL" : "postgres://user:michael@localhost:5432/my_app_name"
}
```
ex : production_config.json :
```JSON
{
    "SECRET_KEY" : "blablablabla",
    "DATABASE_URL" : "postgres://user:michael@localhost:5432/myapp_name",
    "EMAIL_HOST_USER" : "user",
    "EMAIL_HOST_PASSWORD" : "password",
    "SECRET_ALLOWED_HOST" : "http://xxx.xxx.x.xxx"
}
```

**NE PAS OUBLIER DE CONFIGURER .gitignore à la racine du projet**
```
__pycache__/
\*.py[cod]
.env
venv/
\*.sqlite3
env_configuration/
```

AUTRE EX settings/production.py :

```Python
from ..settings.base import *
DEBUG = False
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
env_config_file = BASE_DIR + '/env_configuration/production_config.json'

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

EMAIL_HOST_USER = get_env_var('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_var('EMAIL_HOST_PASSWORD')
SECRET_ALLOWED_HOST = get_env_var('SECRET_ALLOWED_HOST')

ALLOWED_HOSTS = [SECRET_ALLOWED_HOST,]

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

```

### 2. Configurer par défaut le fichier wsgi.py avec la version de prod par défaut pour éviter les mauvaises surprises de mettre un environnement de dev en production :

```Python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analyzer_api.settings.production')
application = get_wsgi_application()
```

Remarque : pour lancer gunicorn avec un environnement différent, you can use the –env option to set the path to load the settings. In case you need it you can also add your application path to PYTHONPATH using the –pythonpath option:
```Bash
$ gunicorn --env DJANGO_SETTINGS_MODULE=myproject.settings myproject.wsgi
$ gunicorn --env DJANGO_SETTINGS_MODULE= analyzer_api.settings.local analyzer_api.wsgi
```


## SUR LE SERVEUR

### 1. Installation NGINX : serveur web : léger et facile à configurer
voir la version os de linux sur le serveur :
```Bash
uname -a
lsb_release -a

sudo apt-get update
sudo apt-get install nginx

#vérifier la version :
nginx -v
```

configuration de nginx : créer ce fichier dans ** */Etc/nginx/sites-available* **
puis créer un symlink in ** _ /etc/nginx/sites-enabled _ ** : (voir ci-dessous)
```Bash
# create this file in /etc/nginx/sites_available
# and create a symlink in sites-enabled with
# cd /etc/nginx/sites-enabled
# ln -s ../sites-available/this_file_name_you_chose
# (sudo) systemctl enable nginx.service
# (sudo) systemctl start nginx

# Configuration du server
server {
    # use 'listen 80 deferred;' for Linux instead of listen 80;
    # use 'listen 80 accept_filter=httpready;' for FreeBSD
    listen 80 deferred;
    client_max_body_size 4G;

    # set the correct host(s) for your site
    server_name example.com www.example.com;
    server_name 192.168.0.217 127.0.0.1;

    keepalive_timeout 5;
    charset     utf-8;

    access_log /home/elk/app/nginx/django_test_app.log;
    error_log /home/elk/app/nginx/django_test_app.log;

    # path for static files
    # root /home/elk/app/django_test/static;

    # Fichiers media et statiques, délivrés par nginx directement
    location /media  {
        autoindex on;
        alias /home/elk/app/django_test/media;
    }

    location /static {
        autoindex on;
        alias /home/elk/app/django_test/static;
    }

    location / {
    # checks for static file, if not found proxy to app
        try_files $uri @proxy_to_app;
    }

    # Le reste va vers notre proxy uwsgi
    location @proxy_to_app {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        # we don't want nginx trying to do something clever with
        # redirects, we set the Host: header above already.
        proxy_redirect off;
        proxy_pass http://unix:/run/gunicorn/socket;
    }

    error_page 500 502 503 504 /500.html;
    location = /500.html {
      root /home/elk/app/django_test/static;
    }
}

```
Lancer NGINX en service:
```Bash
(sudo) systemctl enable nginx.service
(sudo) systemctl start nginx
```

Autre commande Start NGINX : sudo nginx
vérify that NGINX open source is up and running :
curl -I 127.0.0.1
(en local sinon mettre l’adresse ip du serveur)


### 2. Installer miniconda (plus léger qu’Anaconda) :
télécharger le fichier d’installation en 3.7 (ou dernière version) :
	- Miniconda  sur https://conda.io/miniconda.html
	- Anaconda sur https://www.anaconda.com/download/#linux

lancer le fichier d’install :
```Bash
bash Miniconda3-latest-Linux-x86_64.sh
```
(répondre yes),
relancer le terminal

vérifier l’installation : conda list
vérifier que le PATH a été mis à jour pour regarder dans le dossier bin de miniconda3 :
```Bash
$ echo $PATH
$ which python
```
python doit désormais être trouvé dans miniconda. Avant chaque nouvelle install, il peut être utile de faire désormais une mise à jour de conda : conda update conda

Principales commandes pour gérer les environnements virtuels :
- Liste des environnements : conda info --envs. (l’environnement actif est indiqué avec une astérisque \*)
- Création simple de l’environnement nommé myenv : conda create --name myenv. (ou -n)
- Création avec installation de paquets (ici numpy et scipy) : conda create --name myenv numpy scipy.
- Création avec version spécifique de Python : conda create --name myenv python=3.6.
- Création avec version spécifique de paquets : conda create --name myenv numpy=1.19 scipy=0.15.
- Version de Python dans l’environnement : python --version.
- Activer un environnement (ici myenv) : source activate myenv.
- Déactiver l’environnement actif : source deactivate.
- Supprimer un environnement (il doit être désactiver, ici myenv) : conda env remove –name
conda remove --name myenv --all
-rechercher un paquet avec conda : conda search <name>
- installer un paquet : conda install <name>
- vérifier la liste des paquets : conda list
- update a package : conda update <name>


### 3. Installer l’application django avec git
vérifier si git est présent : git --version
générer une clé ssh :
```Bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```
ajouter la clé id_rsa.pub au repo bitbucket : pour la copier-coller, il faut l’afficher :
```Bash
cat ~/.ssh/id_rsa.pub
```

créer un dossier pour l’application :mkdir ~/app && cd $_
si besoin ajouter le hostname dans la liste des hosts connus : sudo nano /etc/hosts
```Bash
192.168.0.212   git.poietis.com         git
```

Cloner le repo dans le dossier du serveur :
git clone ssh://git@git.xxxxx.com:yyyyyyyy/dathub/django_test.git


### 4. Installer un environnement django avec Conda :
créer un environnement :
```Bash
conda create --name django_env python=3.7
```

installer django :
```Bash
conda install django
```

Mais mieux : créer un environnement similaire à l’environnement de dev avec les bons paquets
dans l’environnement de dev lancer la commande : conda list --explicit > spec-conda.txt

créer aussi un duplicata des paquets installés avec pip via un : pip freeze > requirements.txt
et le mettre sur le partage git
puis créer un environnement avec :
```Bash
conda create --name myenv --file spec-file.txt
```

Vérifier dans requiremetns.txt ce qui manque en installation conda, et installer avec conda ce qui manque via conda search <name> puis conda install <name> (au pire pip install xxxxxxx)


### 5. Installer gunicorn

=> serveur semblable au serveur de dev qui exécute le projet Django et qui fait office de serveur HTTP WSGI (à lier à NGINX). NGINX will receive all requests to the server. All it is going to do is decide if the requested information is a static asset that it can serve by itself, or if it’s something more complicated. If so, it will pass the request to Gunicorn. The NGINX will also be configured with HTTPS certificates. Meaning it will only accept requests via HTTPS. If the client tries to request via HTTP, NGINX will first redirect the user to the HTTPS, and only then it will decide what to do with the request. Gunicorn is an application server. Depending on the number of processors the server has, it can spawn multiple workers to process multiple requests in parallel. It manages the workload and executes the Python and Django code. Django is the one doing the hard work. It may access the database (PostgreSQL) or the file system. But for the most part, the work is done inside the views, rendering templates, all those things that we’ve been coding for the past weeks. After Django process the request, it returns a response to Gunicorn, who returns the result to NGINX that will finally deliver the response to the client. We are also going to install PostgreSQL, a production quality database system. Because of Django’s ORM system, it’s easy to switch databases. The last step is to install Supervisor. It’s a process control system and it will keep an eye on Gunicorn and Django to make sure everything runs smoothly. If the server restarts, or if Gunicorn crashes, it will automatically restart it.


mettre à jour pip :
```Bash
pip install -U pip
pip install gunicorn
```
ou mieux si conda :
```Bash
conda install gunicorn
```

création d’un fichier de lancement de la commande gunicorn avec des paramètres précis : ex : launch_gunicorn ou launch_gunicorn.sh

le mettre dans /usr/local/bin  pour les commandes créées par l’utilisateur et lui donner les droits d’exécution :
```Bash
sudo chmod +x launch_gunicorn
```
```Bash
#!/bin/bash
#should be launched in sudo if permission needed for editing logfile
# this file has to be copied in /usr/local/bin and : sudo chmod +x path_to_this_file
set -e
LOGFILE=/var/log/gunicorn/djangoapp.log
LOGDIR=$(dirname $LOGFILE)
LOGLEVEL=debug   # info ou warning une fois l'installation OK
NUM_WORKERS=3    # Règle : (2 x $num_cores) + 1
TIMEOUT=120
# user/group to run as
USER=elk
GROUP=elk

PATH=/home/elk/miniconda3/envs/watcher_env/bin:/home/elk/miniconda3/bin:$PATH

# specify the name of the django app
app_name=analyzer_api

cd /home/elk/app/django_test
# source ../bin/activate  # Cette ligne ne sert que si vous utilisez virtualenv
source activate django_env # si on utilise conda (avec systectl il faut configurer le PATH d’abord et il faut créer son environnement au préalable)
test -d $LOGDIR || mkdir -p $LOGDIR
if [ ! -d $LOGFILE ]
then
        touch $LOGFILE
fi
exec gunicorn --pid /run/gunicorn/pid -w $NUM_WORKERS --timeout $TIMEOUT\
  --user=$USER --group=$GROUP --log-level=$LOGLEVEL \
  --log-file=$LOGFILE 2>>$LOGFILE --bind unix:/run/gunicorn/socket $app_name.wsgi
```

rq : le pid (process id) défini ici est celui défini dans le service nginx (voir plus loin)

ce fichier lance un serveur gunicorn et le bind sur un socket en lien avec NGINX : il faut le lancer en tâche de fond : le mettre en daemon avec systemd ou le lancer :  puis le mettre en background via ctrl-Z et taper bg

(NB : gunicorn_django deprecated parce que intégré dans django, donc juste gunicorn command)


créer un service :
gunicorn.service
```Bash
# copy this file to /etc/systemd/system/gunicorn.service or /lib/systemd/system/gunicorn.service
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
PIDFile=/run/gunicorn/pid
User=elk
Group=elk
RuntimeDirectory=gunicorn
WorkingDirectory=/home/elk/app/django_test
ExecStart=/usr/local/bin/launch_gunicorn
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

il faut créer un service socket :
gunicorn.socket
```Bash
# this file has to be copied in /etc/systemd/system/gunicorn.socket
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn/socket

[Install]
WantedBy=sockets.target
```

il faut créer un fichier de conf pour le service gunicorn :
gunicorn.conf

```Bash
# this file has to be copied in /etc/tmpfiles.d/gunicorn.conf
d /run/gunicorn 0755 elk elk -
```
ou :  d /run/gunicorn 0755 someuser somegroup -

Puis dans le terminal :
```Bash
sudo systemctl daemon-reload
sudo systemctl enable gunicorn.socket
sudo systemctl start gunicorn.socket
```
le service gunicorn.service devrait se lancer automatiquement quand le socket est utilisé mais on peut l’activer au cas où :
```Bash
(sudo) systemctl start gunicorn.service
```
pour utiliser le service : plusieurs commandes
```Bash
sudo systemctl start/restart/stop gunicorn.service
```
en cas de modification du service :
```Bash
sudo systemctl daemon-reload
```
