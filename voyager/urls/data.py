from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from humfrey.desc import views as desc_views
from humfrey.elasticsearch import views as elasticsearch_views
from humfrey.thumbnail import views as thumbnail_views
from humfrey.misc import views as misc_views
from humfrey.sparql.views import admin as sparql_admin_views
from humfrey.sparql.views import core as sparql_core_views

from voyager.core import views as core_views

#from humfrey.dataox.views import DatasetView, ExploreView, ExampleDetailView, ExampleResourceView, ExampleQueryView, ContactView, ForbiddenView, HelpView, ResizedImageView

urlpatterns = patterns('',
    url(r'^$', misc_views.SimpleView.as_view(template_name="index"), name='index'),
    url(r'^id/.*$', desc_views.IdView.as_view(), name='id'),

    url(r'^doc.+$', desc_views.DocView.as_view(), name='doc'),
    url(r'^doc/$', desc_views.DocView.as_view(), name='doc-generic'),
    url(r'^desc/$', desc_views.DescView.as_view(), name='desc'),

    url(r'^search/$', elasticsearch_views.SearchView.as_view(), name='search'),
    url(r'^elasticsearch/(?:(?P<index>[A-Z\-\d]+)/)?$',
        sparql_admin_views.ElasticSearchPassThroughView.as_view(), #uri_lookup_url='/doc/',
                                                                #sparql_endpoint_url='/sparql/'),
        {'store': 'public'}, name='elasticsearch'),

    url(r'^objects/$', core_views.ObjectCategoryView.as_view(), name='claros-objects'),
    url(r'^objects/(?P<ptype>[a-z\-_]+)/$', core_views.ObjectView.as_view(), name='claros-objects-detail'),

    url(r'^people/$', core_views.PeopleView.as_view(), name='claros-people'),
    url(r'^people/(?P<page>[1-9]\d*)/$', core_views.PeopleView.as_view(), name='claros-people-page'),

    url(r'^places/', include('voyager.places.urls', 'places')),
    url(r'^nearby/$', core_views.NearbyView.as_view(), name='nearby'),

    url(r'^sparql/', include('humfrey.sparql.urls.simple', 'sparql')),
    url(r'^graph/(?P<path>.*)$', sparql_core_views.GraphStoreView.as_view(), name='graph-store'),

    url(r'^forbidden/$', misc_views.SimpleView.as_view(context={'status_code': 403},
                                                       template_name='forbidden'), name='forbidden'),

    url(r'^pingback/', include('humfrey.pingback.urls', 'pingback')),

    url(r'^thumbnail/$', thumbnail_views.ThumbnailView.as_view(), name='thumbnail'),
) + staticfiles_urlpatterns()

handler404 = misc_views.SimpleView.as_view(context={'status_code': 404}, template_name='404')
handler500 = misc_views.SimpleView.as_view(context={'status_code': 500}, template_name='500')

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^site-media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )

