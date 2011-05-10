from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import redirect_to

from humfrey.desc.views import IndexView, IdView, DocView, SparqlView
#from humfrey.dataox.views import DatasetView, ExploreView, ExampleDetailView, ExampleResourceView, ExampleQueryView, ContactView, ForbiddenView, HelpView, ResizedImageView

import resource

urlpatterns = patterns('',
    (r'^$', IndexView(), {}, 'index'),
    (r'^id/.*$', IdView(), {}, 'id'),
    (r'^doc/.*$', DocView(), {}, 'doc'),
#    (r'^graph/.*$', GraphView(), {}, 'graph'),
#    (r'^datasets/$', DatasetView(), {}, 'datasets'),
    (r'^sparql/$', SparqlView(), {}, 'sparql'),
#    (r'^contact/$', ContactView(), {}, 'contact'),
#    (r'^help/$', HelpView(), {}, 'help'),

#    (r'^forbidden/$', ForbiddenView(), {}, 'forbidden'),

#    (r'^explore/$', ExploreView(), {}, 'explore'),
#    (r'^explore/resources/$', ExampleResourceView(), {}, 'explore-resource'),
#    (r'^explore/queries/$', ExampleQueryView(), {}, 'explore-query'),

#    (r'^explore/(?P<slug>[a-z\d-]+)/$', ExampleDetailView(), {}, 'example-detail'),
#    (r'^explore/example:(?P<slug>[a-z\d-]+)/$', redirect_to, {'url': '/explore/%(slug)s/'}),

#    (r'^external-image/$', ResizedImageView(), {}, 'resized-image'),    
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^site-media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )

