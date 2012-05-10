from __future__ import absolute_import
import imp
import os

from humfrey.settings.common import *

ADMINS = (
    ('Open Data at OUCS', 'opendata@oucs.ox.ac.uk'),
)

MANAGERS = ADMINS

DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql_psycopg2',
                         'NAME': 'voyager'}}

INSTALLED_APPS += (
    'voyager.core',
    'voyager.places',
    'voyager.search',
    'humfrey.sparql',
    'django_hosts',
    'django.contrib.admin',
)

AUTHENTICATION_BACKENDS = (
    'object_permissions.backend.ObjectPermBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    'django.core.context_processors.request',
    "django.contrib.messages.context_processors.messages",
    "voyager.core.context_processors.base_template_chooser"
)
MEDIA_URL = '//data.clarosnet.org/site-media/'

MIDDLEWARE_CLASSES = ('django_hosts.middleware.HostsMiddleware',) + MIDDLEWARE_CLASSES

ROOT_URLCONF = 'voyager.urls.empty'
ROOT_HOSTCONF = 'voyager.hosts'
DEFAULT_HOST = 'empty'
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), '..', 'dataox', 'templates'),
)

IMAGE_TYPES += ('crm:E38_Image',)
IMAGE_PROPERTIES += ('crm:P138i_has_representation',)

ADDITIONAL_NAMESPACES = {
    'crm': 'http://purl.org/NET/crm-owl#',
    'claros': 'http://purl.org/NET/Claros/vocab#',
}

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
) + TEMPLATE_DIRS

ID_MAPPING = (
    ('http://id.clarosnet.org/', 'http://data.clarosnet.org/doc/', True),
    ('http://www.mae.u-paris10.fr/limc-france/LIMC-objet.php?code_objet=', 'http://data.clarosnet.org/doc:limc/object/', False),
    ('http://www.mae.u-paris10.fr/limc-france/images/', 'http://data.clarosnet.org/doc:limc/image/', False),
    ('http://www.lgpn.ox.ac.uk/id/', 'http://data.clarosnet.org/doc:lgpn/person/', False),
    ('http://www.lgpn.ox.ac.uk/placecode/', 'http://data.clarosnet.org/doc:lgpn/place/', False),
    ('http://www.lgpn.ox.ac.uk/coordinates/', 'http://data.clarosnet.org/doc:lgpn/coordinates/', False),
    ('http://www.lgpn.ox.ac.uk/placename/', 'http://data.clarosnet.org/doc:lgpn/placename/', False),
    ('http://jameelcentre.ashmolean.org/', 'http://data.clarosnet.org/doc:jameel/', False),
    ('http://arachne.uni-koeln.de/', 'http://data.clarosnet.org/doc:arachne/', False),
    ('http://purl.org/NET/crm-owl#', 'http://data.clarosnet.org/doc:crm/', False),
)

SERVED_DOMAINS = (
    'id.clarosnet.org',
    'data.clarosnet.org',
)

UPDATE_FILES_DIRECTORY = os.path.join(MEDIA_ROOT, 'update-files')

STATIC_ROOT = relative_path(config.get('main:static_root'))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), 'static'),
    os.path.join(imp.find_module('humfrey')[1], 'static'),
)

LOGIN_URL = '/login/'

ANONYMOUS_USER_ID = 0