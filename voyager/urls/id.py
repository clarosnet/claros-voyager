from django.conf.urls import *

from humfrey.desc import views as desc_views
from humfrey.misc import views as misc_views

urlpatterns = patterns('',
    (r'', desc_views.IdView.as_view(), {}, 'id'),
)


handler404 = misc_views.SimpleView.as_view(context={'status_code': 404}, template_name='404-id')
handler500 = misc_views.SimpleView.as_view(context={'status_code': 500}, template_name='500')
