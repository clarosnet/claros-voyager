import json
import random
import rdflib
import urllib2
from collections import defaultdict

from django.http import Http404, HttpResponsePermanentRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django_conneg.views import HTMLView, ContentNegotiatedView

from humfrey.elasticsearch.views import SearchView
from humfrey.results.views.standard import RDFView, ResultSetView
from humfrey.linkeddata.resource import Resource
from humfrey.linkeddata.views import MappingView
from humfrey.sparql.views import StoreView
from humfrey.utils.namespaces import NS

class ObjectCategoryView(HTMLView, RDFView, StoreView, MappingView):
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

    def get(self, request):
        graph, subjects = self.get_object_types(self.endpoint)

        context = {
            'graph': graph,
            'subjects': subjects,
            'queries': [graph.query],
        }
        return self.render(request, context, 'claros/objects-index')

class ObjectView(HTMLView, RDFView, StoreView, MappingView):
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

    def get(self, request, ptype):
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

        context = {
            'type': type_resource,
            'types': types,
            'graph': graph,
            'subjects': subjects,
            'queries': [graph.query],
        }

        return self.render(request, context, 'claros/objects')

class PeopleView(HTMLView, ResultSetView, StoreView, MappingView):
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

    def get(self, request, page=None):
        if page:
            page = int(page)
            if page == 1:
                return HttpResponsePermanentRedirect(reverse('claros-people'))
        else:
            page = 1

        results = self.endpoint.query(self._query % ((page-1)*1000))
        people = defaultdict(lambda:defaultdict(set))
        for result in results:
            person = people[result.person]
            person['uri'] = result.person
            person['appellations'].add(result.appellation)
            person['birth_period_label'] = result.birth_period_label
            person['birth_place'] = result.birth_place
            person['birth_place_label'] = result.birth_place_label
        people = people.values()

        context = {
            'results': results,
            'people': people,
            'page': page,
            'queries': [results.query],
        }
        return self.render(request, context, 'claros/people')


class NearbyView(MappingView, HTMLView):
    query_url = 'http://localhost:3030/public/man-made-object/_search'
    query_url = 'http://data.clarosnet.org/elasticsearch/'
    def get(self, request):
        try:
            lat, lon, distance = (float(request.GET[x]) for x in ('lat', 'lon', 'distance'))
        except (ValueError, KeyError):
            return HttpResponseBadRequest()

        query = {'query': {'filtered': {
                    'query': {'match_all': {}},
                    'filter': {'geo_distance': {'distance': '{0}km'.format(distance),
                                                'findLocation.location': {'lat': lat, 'lon': lon}}}}},
                 'sort': [
                     {'_geo_distance': {'findLocation.location': {'lat': lat, 'lon': lon},
                                        'order': 'asc', 'unit': 'km'}}],
                 'from': 0,
                 'size': 1000}

        response = urllib2.urlopen(self.query_url, json.dumps(query))
        results = SearchView.Deunderscorer(json.load(response))

        context = {'lat': lat,
                   'lon': lon,
                   'distance': distance,
                   'results': results}

        return self.render(request, context, 'claros/nearby')
