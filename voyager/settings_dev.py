from .settings_base import *

DEBUG = True
STAGING = True

SECRET_KEY = 'i9rWtMoaQ8y9QtvilgC8KnmKidbRfLz7'

STATIC_ROOT = os.path.join(os.path.dirname(__file__),
                           'static-collected')

IMAGE_CACHE_DIRECTORY = os.path.join(os.path.dirname(__file__),
                                     'image-cache')
