from __future__ import absolute_import
import os

from humfrey.settings.common import *

ADMINS = (
    ('Open Data at OUCS', 'opendata@oucs.ox.ac.uk'),
)

MANAGERS = ADMINS

ENDPOINT_URL = 'http://localhost:8080/claros_server-1.0/endpoint/combined'

INSTALLED_APPS += (
    'voyager.core',
    'django_hosts',
)

MIDDLEWARE_CLASSES = ('django_hosts.middleware.HostsMiddleware',) + MIDDLEWARE_CLASSES

ROOT_URLCONF = 'voyager.urls'
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
    ('http://id.clarosnet.org/', 'http://data.clarosnet.org:8000/doc/', True),
    ('http://www.mae.u-paris10.fr/limc-france/LIMC-objet.php?code_objet=', 'http://data.clarosnet.org:8000/doc:limc/', False),
)

SERVED_DOMAINS = (
    'id.clarosnet.org',
    'data.clarosnet.org',
)
