from django.conf.urls.defaults import *

from humfrey.desc.views import IdView

urlpatterns = patterns('',
    (r'', IdView(), {}, 'id'),
)
