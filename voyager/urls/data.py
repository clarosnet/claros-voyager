from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from humfrey.desc import views as desc_views
from humfrey.images import views as images_views
from humfrey.sparql import views as sparql_views
from humfrey.misc import views as misc_views

from voyager.core import views as core_views

#from humfrey.dataox.views import DatasetView, ExploreView, ExampleDetailView, ExampleResourceView, ExampleQueryView, ContactView, ForbiddenView, HelpView, ResizedImageView

urlpatterns = patterns('',
    url(r'^$', misc_views.FeedView.as_view(rss_url="http://clarosdata.wordpress.com/feed/",
                                        template_name="index"), name='index'),
    url(r'^id/.*$', desc_views.IdView.as_view(), name='id'),

    url(r'^doc.+$', desc_views.DocView.as_view(), name='doc'),
    url(r'^doc/$', desc_views.DocView.as_view(), name='doc-generic'),
    url(r'^desc/$', desc_views.DescView.as_view(), name='desc'),
    
    url(r'^search/$', include('voyager.search.urls', 'search')),

    url(r'^objects/$', core_views.ObjectCategoryView.as_view(), name='claros-objects'),
    url(r'^objects/(?P<ptype>[a-z-]+)/$', core_views.ObjectView.as_view(), name='claros-objects-detail'),

    url(r'^people/$', core_views.PeopleView.as_view(), {}, 'claros-people'),
    url(r'^people/(?P<page>[1-9]\d*)/$', core_views.PeopleView.as_view(), name='claros-people-page'),

    url(r'^places/$', include('voyager.places.urls', 'places')),

    url(r'^sparql/', include('humfrey.sparql.urls', 'sparql')),

    url(r'^forbidden/$', misc_views.SimpleView.as_view(context={'status_code': 403},
                                                    template_name='forbidden'), name='forbidden'),

    url(r'^pingback/', include('humfrey.pingback.urls.public', 'pingback')),

    url(r'^external-image/$', images_views.ResizedImageView.as_view(), name='resized-image'),
)

handler404 = misc_views.SimpleView.as_view(context={'status_code': 404}, template_name='404')
handler500 = misc_views.SimpleView.as_view(context={'status_code': 500}, template_name='500')

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^site-media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )

