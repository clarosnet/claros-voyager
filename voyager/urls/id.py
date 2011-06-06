from django.conf.urls.defaults import *

from humfrey.desc.views import IdView

from voyager.core.views import NotFoundView, ServerErrorView

urlpatterns = patterns('',
    (r'', IdView(), {}, 'id'),
)

handler404 = NotFoundView('404-id')
handler500 = ServerErrorView()