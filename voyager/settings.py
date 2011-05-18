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
)

ROOT_URLCONF = 'voyager.urls'
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
