from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from humfrey.desc import views as desc_views
from humfrey.images import views as images_views
from humfrey.sparql import views as sparql_views
from humfrey.misc import views as misc_views

from voyager.core import views as core_views

#from humfrey.dataox.views import DatasetView, ExploreView, ExampleDetailView, ExampleResourceView, ExampleQueryView, ContactView, ForbiddenView, HelpView, ResizedImageView

urlpatterns = patterns('',
    (r'^$', misc_views.FeedView.as_view(rss_url="http://clarosdata.wordpress.com/feed/",
                                        template_name="index"), {}, 'index'),
    (r'^id/.*$', desc_views.IdView.as_view(), {}, 'id'),

    (r'^doc.+$', desc_views.DocView.as_view(), {}, 'doc'),
    (r'^doc/$', desc_views.DocView.as_view(), {}, 'doc-generic'),
    (r'^desc/$', desc_views.DescView.as_view(), {}, 'desc'),
    
    (r'^objects/$', core_views.ObjectCategoryView.as_view(), {}, 'claros-objects'),
    (r'^objects/(?P<ptype>[a-z-]+)/$', core_views.ObjectView.as_view(), {}, 'claros-objects-detail'),

    (r'^people/$', core_views.PeopleView.as_view(), {}, 'claros-people'),
    (r'^people/(?P<page>[1-9]\d*)/$', core_views.PeopleView.as_view(), {}, 'claros-people-page'),

    (r'^sparql/$', sparql_views.SparqlView.as_view(), {}, 'sparql'),

    (r'^forbidden/$', misc_views.SimpleView.as_view(context={'status_code': 403},
                                                    template_name='forbidden'), {}, 'forbidden'),

    (r'^pingback/', include('humfrey.pingback.urls', 'pingback')),

    (r'^external-image/$', images_views.ResizedImageView.as_view(), {}, 'resized-image'),    
)

handler404 = misc_views.SimpleView.as_view(context={'status_code': 404}, template_name='404')
handler500 = misc_views.SimpleView.as_view(context={'status_code': 500}, template_name='500')

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^site-media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )

