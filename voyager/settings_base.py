import imp
import os

DEBUG = False
STAGING = False

# Localization
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'

INTERNAL_IPS = (
    '127.0.0.1',       # localhost
    '129.67.101.12',   # oucs-alexd.oucs.ox.ac.uk
    '192.168.122.1',   # virt-manager host
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django_conneg',
    'django_hosts',
    'django_webauth',
    'guardian',
    'humfrey.desc',
    'humfrey.elasticsearch',
    'humfrey.sparql',
    'humfrey.streaming',
    'humfrey.update',
    'humfrey.manage',
    'humfrey.pingback',
    'humfrey.thumbnail',
    'humfrey.utils',
    'voyager.core',
    'voyager.places',
    'djcelery',
    'raven.contrib.django',
)

MIDDLEWARE_CLASSES = (
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'django_hosts.middleware.HostsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'humfrey.base.middleware.AccessControlAllowOriginMiddleware',
    'django_conneg.support.middleware.BasicAuthMiddleware',
    'humfrey.pingback.middleware.PingbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ANONYMOUS_USER_ID = 0

DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql_psycopg2',
                         'NAME': 'humfrey-voyager'}}

MANAGERS = ADMINS = ()

ROOT_URLCONF = 'voyager.urls.empty'
ROOT_HOSTCONF = 'voyager.hosts'
DEFAULT_HOST = 'data'

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), 'static'),
    os.path.join(imp.find_module('humfrey')[1], 'static'),
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

DEFAULT_STORE = 'public'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), '..', 'dataox', 'templates'),
)

IMAGE_TYPES = ('foaf:Image', 'crm:E38_Image')
IMAGE_PROPERTIES = ('foaf:depiction', 'crm:P138i_has_representation')

ADDITIONAL_NAMESPACES = {
    'crm': 'http://purl.org/NET/crm-owl#',
    'claros': 'http://purl.org/NET/Claros/vocab#',
}

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
) + TEMPLATE_DIRS

THUMBNAIL_URL = ('data', 'thumbnail')

ID_MAPPING = (
#    ('http://id.clarosnet.org/', 'http://data.clarosnet.org/doc/', True),
#    ('http://www.mae.u-paris10.fr/limc-france/LIMC-objet.php?code_objet=', 'http://data.clarosnet.org/doc:limc/object/', False),
#    ('http://www.mae.u-paris10.fr/limc-france/images/', 'http://data.clarosnet.org/doc:limc/image/', False),
#    ('http://www.lgpn.ox.ac.uk/id/', 'http://data.clarosnet.org/doc:lgpn/person/', False),
#    ('http://www.lgpn.ox.ac.uk/placecode/', 'http://data.clarosnet.org/doc:lgpn/place/', False),
#    ('http://www.lgpn.ox.ac.uk/coordinates/', 'http://data.clarosnet.org/doc:lgpn/coordinates/', False),
#    ('http://www.lgpn.ox.ac.uk/placename/', 'http://data.clarosnet.org/doc:lgpn/placename/', False),
#    ('http://jameelcentre.ashmolean.org/', 'http://data.clarosnet.org/doc:jameel/', False),
#    ('http://arachne.uni-koeln.de/', 'http://data.clarosnet.org/doc:arachne/', False),
#    ('http://purl.org/NET/crm-owl#', 'http://data.clarosnet.org/doc:crm/', False),
)

SERVED_DOMAINS = (
    'id.clarosnet.org',
    'data.clarosnet.org',
)

ANONMYMOUS_USER_ID = 0

ELASTICSEARCH_SERVER = {'host': 'localhost',
                        'port': 9200}

DOC_RDF_PROCESSORS = (
    'humfrey.desc.rdf_processors.doc_meta',
    'humfrey.desc.rdf_processors.formats',
)

REDIS_PARAMS = {'host': 'localhost',
                'port': 6379}

BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis"
CELERY_REDIS_HOST = "localhost"
CELERY_REDIS_PORT = 6379
CELERY_REDIS_DB = 0
CELERY_IMPORTS = (
    'humfrey.archive.tasks',
    'humfrey.ckan.tasks',
    'humfrey.elasticsearch.tasks',
    'humfrey.update.tasks',
)
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERYD_LOG_LEVEL = 'DEBUG'
