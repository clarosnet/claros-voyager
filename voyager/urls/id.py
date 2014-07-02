from django.conf.urls import patterns, url
from django_hosts import reverse_full

from humfrey.desc import views as desc_views
from humfrey.misc import views as misc_views

class IdView(desc_views.IdView):
    @property
    def doc_view(self):
        return reverse_full('data', 'doc-generic')
    @property
    def desc_view(self):
        return reverse_full('data', 'desc')

urlpatterns = patterns('',
    url(r'^.*', IdView.as_view(), {}, 'id'),
)


handler404 = misc_views.SimpleView.as_view(context={'status_code': 404}, template_name='404-id')
handler500 = misc_views.SimpleView.as_view(context={'status_code': 500}, template_name='500')
