from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from humfrey.misc import views as misc_views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', login_required(misc_views.SimpleView.as_view(template_name='manage')), name='index'),
    url(r'^update/', include('humfrey.update.urls', 'update')),
    url(r'^stores/', include('humfrey.sparql.urls.admin', 'sparql-admin')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
) + staticfiles_urlpatterns()

handler404 = misc_views.SimpleView.as_view(context={'status_code': 404}, template_name='404')
handler500 = misc_views.SimpleView.as_view(context={'status_code': 500}, template_name='500')
