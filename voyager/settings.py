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
    ('http://www.mae.u-paris10.fr/limc-france/LIMC-objet.php?code_objet=', 'http://data.clarosnet.org/doc:limc/', False),
    ('http://www.lgpn.ox.ac.uk/id/', 'http://data.clarosnet.org/doc:lgpn/person/', False),
    ('http://www.lgpn.ox.ac.uk/placecode/', 'http://data.clarosnet.org/doc:lgpn/place/', False),
    ('http://www.lgpn.ox.ac.uk/coordinates/', 'http://data.clarosnet.org/doc:lgpn/coordinates/', False),
    ('http://www.lgpn.ox.ac.uk/placename/', 'http://data.clarosnet.org/doc:lgpn/placename/', False),
    ('http://jameelcentre.ashmolean.org/', 'http://data.clarosnet.org/doc:jameel/', False),
    ('http://arachne.uni-koeln.de/', 'http://data.clarosnet.org/doc:arachne/', False),
)

SERVED_DOMAINS = (
    'id.clarosnet.org',
    'data.clarosnet.org',
)

