import random
from collections import defaultdict

from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse

from humfrey.desc.views import EndpointView, RDFView, SRXView
from humfrey.utils.resource import Resource
from humfrey.utils.namespaces import NS
from humfrey.utils.views import BaseView
from humfrey.utils.cache import cached_view

class ObjectView(EndpointView, RDFView):
    _graph_names = [
        'http://purl.org/NET/Claros/graph/metamorphoses',
        'http://purl.org/NET/Claros/graph/lgpn',
        'http://purl.org/NET/Claros/graph/arachne',
        'http://purl.org/NET/Claros/graph/ashmol',
        'http://purl.org/NET/Claros/graph/beazley_pottery',
        'http://purl.org/NET/Claros/graph/beazley_gems',
        'http://purl.org/NET/Claros/graph/beazley_casts',
        'http://purl.org/NET/Claros/graph/beazley_photos',
        'http://purl.org/NET/Claros/graph/creswell',
        'http://purl.org/NET/Claros/graph/limc',
    ]
    
    _query = """
        CONSTRUCT {
            ?obj rdfs:label ?label ; crm:P138i_has_representation ?image
        } WHERE {
          """ + " UNION ".join("""
              { SELECT ?obj ?image ?label WHERE {
                  GRAPH <%s> {
                      ?obj crm:P138i_has_representation ?image ; rdfs:label ?label .
                      MINUS { ?image crm:P2_has_type claros:Thumbnail }
                  }
              } LIMIT 1000 }""" % graph_name for graph_name in _graph_names) + """
        }
    """
    
    _query = """
      PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      PREFIX  crm:  <http://purl.org/NET/crm-owl#>
      PREFIX  claros: <http://purl.org/NET/Claros/vocab#hasLiteral>
   
      CONSTRUCT {
        ?obj rdfs:label ?label .
        ?obj crm:P138i_has_representation ?image
      } WHERE {
        GRAPH <http://purl.org/NET/Claros/graph/arachne> {
          ?obj crm:P138i_has_representation ?image .
          ?obj rdfs:label ?label .
          MINUS { ?image crm:P2_has_type claros:Thumbnail } .
        }
      } LIMIT 2000
    """
    
    # FILTER ( ?image != <http://www.beazley.ox.ac.uk/Vases/SPIFF//cc001001.jpe>
    #       && ?image != <http://www.beazley.ox.ac.uk/Vases/SPIFF//ac001001.jpe> )

    @cached_view
    def handle_GET(self, request, context):
        if not hasattr(self, '_cached_graph'):
            self._cached_graph = self.endpoint.query(self._query)
        graph = self._cached_graph
        subjects = set(graph.subjects(NS['crm'].P138i_has_representation))
        subjects = [Resource(s, graph, self.endpoint) for s in subjects]
        random.shuffle(subjects)
        subjects = subjects[:200]
        context.update({
            'graph': graph,
            'subjects': subjects,
        })
        return self.render(request, context, 'claros/objects')

class PeopleView(EndpointView, SRXView):
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

        results = list(self.endpoint.query(self._query % ((page-1)*1000)))
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
        })
        return self.render(request, context, 'claros/people')



class ForbiddenView(BaseView):
    @cached_view
    def handle_GET(self, request, context):
        context['status_code'] = 403
        return self.render(request, context, 'forbidden')
