import random
from collections import defaultdict

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
                      MINUS { ?image crm:P2_has_type claros:Thumbnail } .
                      FILTER ( matches('SPIFF//', ?image) )
                  }
              } LIMIT 1 }""" % graph_name for graph_name in _graph_names) + """
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
        GRAPH <http://purl.org/NET/Claros/graph/ashmol> {
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
        graph = self.endpoint.query(self._query, common_prefixes=False)
        subjects = set(graph.subjects(NS['crm'].P138i_has_representation))
        subjects = [Resource(s, graph, self.endpoint) for s in subjects]
        random.shuffle(subjects)
        context.update({
            'graph': graph,
            'subjects': subjects,
        })
        return self.render(request, context, 'claros/objects')

class PeopleView(EndpointView, SRXView):
    _query = """
      SELECT ?person ?appellation ?birth_period_begin ?birth_period_end ?birth_place ?birth_place_name WHERE {
        ?person a crm:E21_Person .
        OPTIONAL { ?person crm:P131_is_identified_by/rdf:value ?appellation } .
        OPTIONAL {
          ?person crm:P98i_was_born ?birth .
          OPTIONAL {
            ?birth crm:P4_has_time-span/crm:P82_at_some_time_within [
              claros:period_begin ?birth_period_begin ;
              claros:period_end ?birth_period_end ] } .
          OPTIONAL {
            ?birth crm:P7_took_place_at ?birth_place .
            OPTIONAL {
              ?birth_place crm:P87_is_identified_by ?place_name }
          }
        }
      } LIMIT 1000
    """

    @cached_view    
    def handle_GET(self, request, context):
        results = list(self.endpoint.query(self._query))
        people = defaultdict(lambda:defaultdict(set))
        for result in results:
        	person = people[result.person.uri]
        	person['uri'] = result.person
        	person['appellations'].add(result.appellation)
        	person['birth_period_begin'] = result.birth_period_begin
        	person['birth_period_end'] = result.birth_period_end
        	person['birth_place'] = result.birth_place
        	person['birth_place_name'].add(result.birth_place_name)
        people = people.values()
        	  
        context.update({
            'results': results,
            'people': people,
        })
        return self.render(request, context, 'claros/people')



class ForbiddenView(BaseView):
    @cached_view
    def handle_GET(self, request, context):
        context['status_code'] = 403
        return self.render(request, context, 'forbidden')