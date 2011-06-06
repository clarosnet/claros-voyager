from django.conf.urls.defaults import *

from voyager.core.views import NotFoundView, ServerErrorView

urlpatterns = patterns('',
)

handler404 = NotFoundView('404-empty')
handler500 = ServerErrorView()