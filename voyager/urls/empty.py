from django.conf.urls.defaults import patterns

from humfrey.misc import views as misc_views

urlpatterns = patterns('',
)

handler404 = misc_views.SimpleView.as_view(context={'status_code': 404}, template_name='404-empty')
handler500 = misc_views.SimpleView.as_view(context={'status_code': 500}, template_name='500')