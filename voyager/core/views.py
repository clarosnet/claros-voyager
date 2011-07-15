import random, rdflib, datetime
from collections import defaultdict

import feedparser, pytz

from django.http import Http404, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from humfrey.linkeddata.views import EndpointView, RDFView, ResultSetView
from humfrey.utils.resource import Resource
from humfrey.utils.namespaces import NS
from humfrey.utils.views import BaseView
from humfrey.utils.cache import cached_view

class IndexView(BaseView):
    def initial_context(self, request):
        try:
            feed = feedparser.parse("http://clarosdata.wordpress.com/feed/")
            for entry in feed.entries:
                entry.updated_datetime = datetime.datetime(*entry.updated_parsed[:6], tzinfo=pytz.utc).astimezone(pytz.timezone(settings.TIME_ZONE))
        except Exception, e:
            feed = None
        return {
            'feed': feed,
        }

    @cached_view
    def handle_GET(self, request, context):
        return self.render(request, context, 'index')

class ObjectCategoryView(EndpointView):
    _query = """
      DESCRIBE ?type WHERE {
        ?type crm:P127_has_broader_term <http://id.clarosnet.org/type/object>
      }
    """

    @classmethod
    def get_object_types(cls, endpoint):
        graph = endpoint.query(cls._query)
        subjects = graph.subjects(NS['crm'].P127_has_broader_term, rdflib.URIRef('http://id.clarosnet.org/type/object'))
        subjects = [Resource(s, graph, endpoint) for s in subjects]
        subjects.sort(key=lambda s:s.rdfs_label)
        for subject in subjects:
            subject.slug = subject._identifier.split('/')[-1]
        return graph, subjects

    def initial_context(self, request):
        graph, subjects = self.get_object_types(self.endpoint)

        return {
            'graph': graph,
            'subjects': subjects,
            'queries': [graph.query],
        }

    def handle_GET(self, request, context):
        return self.render(request, context, 'claros/objects-index')

class ObjectView(EndpointView, RDFView):
    _query = """
      CONSTRUCT {
        ?obj rdfs:label ?label .
        ?obj crm:P138i_has_representation ?image
      } WHERE {
        ?obj crm:P2_has_type %s .
        ?obj crm:P138i_has_representation ?image .
        ?obj rdfs:label ?label .
      } LIMIT 2000
    """

    def initial_context(self, request, ptype):
        type_uri = rdflib.URIRef('http://id.clarosnet.org/type/object/%s' % ptype)
        types = ObjectCategoryView.get_object_types(self.endpoint)[1]

        for t in types:
            if t._identifier == type_uri:
                type_resource = t
                break
        else:
            raise Http404

        graph = self.endpoint.query(self._query % type_uri.n3())
        subjects = graph.subjects(NS['crm'].P138i_has_representation)
        subjects = [Resource(s, graph, self.endpoint) for s in subjects]
        random.shuffle(subjects)
        subjects[200:] = []

        return {
            'type': type_resource,
            'types': types,
            'graph': graph,
            'subjects': subjects,
            'queries': [graph.query],
        }

    @cached_view
    def handle_GET(self, request, context, ptype):
        return self.render(request, context, 'claros/objects')

class PeopleView(EndpointView, ResultSetView):
    _query = """
      SELECT ?person ?appellation ?birth_period_label ?birth_place ?birth_place_label WHERE {
        ?person a crm:E21_Person .
        OPTIONAL { ?person crm:P131_is_identified_by/rdf:value ?appellation } .
        OPTIONAL {
          ?person crm:P98i_was_born ?birth .
          OPTIONAL {
            ?birth crm:P4_has_time-span/rdfs:label ?birth_period_label } .
          OPTIONAL {
            ?birth crm:P7_took_place_at ?birth_place .
            OPTIONAL {
              ?birth_place rdfs:label ?birth_place_label }
          }
        }
      } OFFSET %s LIMIT 1000
    """

    @cached_view    
    def handle_GET(self, request, context, page=None):
        if page:
            page = int(page)
            if page == 1:
                return HttpResponsePermanentRedirect(reverse('claros-people'))
        else:
            page = 1

        results = self.endpoint.query(self._query % ((page-1)*1000))
        people = defaultdict(lambda:defaultdict(set))
        for result in results:
            person = people[result.person.uri]
            person['uri'] = result.person
            person['appellations'].add(result.appellation)
            person['birth_period_label'] = result.birth_period_label
            person['birth_place'] = result.birth_place
            person['birth_place_label'] = result.birth_place_label
        people = people.values()

        context.update({
            'results': results,
            'people': people,
            'page': page,
            'queries': [results.query],
        })
        return self.render(request, context, 'claros/people')

class ForbiddenView(BaseView):
    @cached_view
    def handle_GET(self, request, context):
        context['status_code'] = 403
        return self.render(request, context, 'forbidden')

class NotFoundView(BaseView):
    def __init__(self, template_name):
        super(NotFoundView, self).__init__()
        self._template_name = template_name

    @cached_view
    def handle_GET(self, request, context):
        context['status_code'] = 404
        return self.render(request, context, self._template_name)

class ServerErrorView(BaseView):
    @cached_view
    def handle_GET(self, request, context):
        context['status_code'] = 500
        return self.render(request, context, '500')

