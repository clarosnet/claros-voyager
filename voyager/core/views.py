import random, rdflib
from collections import defaultdict

from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse

from humfrey.desc.views import EndpointView, RDFView, SRXView
from humfrey.utils.resource import Resource
from humfrey.utils.namespaces import NS
from humfrey.utils.views import BaseView
from humfrey.utils.cache import cached_view

class ObjectView(EndpointView, RDFView):
    _query = """
      CONSTRUCT {
        ?obj rdfs:label ?label .
        ?obj crm:P138i_has_representation ?image
      } WHERE {
        %s
      } LIMIT 2000
    """

    _sub_query = """{
          SELECT ?obj ?image ?label WHERE {
            ?obj crm:P2_has_type %s .
            ?obj crm:P138i_has_representation ?image .
            ?obj rdfs:label ?label .
          } LIMIT 500
        }"""

        # Adding this makes it slow
        # MINUS { ?image crm:P2_has_type claros:Thumbnail }
    
    _OBJECT_TYPES = {
        'ceramic':       ('ceramics',      ('http://purl.org/NET/Claros/vocab#Ashmolean/Category/ceramic',
                                            'http://arachne.uni-koeln.de/type/objectType/keramik')),
        'miscellaneous': ('miscellaneous', ('http://purl.org/NET/Claros/vocab#Ashmolean/Category/general',)),
        'print':         ('prints',        ('http://purl.org/NET/Claros/vocab#Ashmolean/Category/print',)),
        'drawing':       ('drawings',      ('http://purl.org/NET/Claros/vocab#Ashmolean/Category/drawing',)),
        'textile':       ('textiles',      ('http://purl.org/NET/Claros/vocab#Ashmolean/Category/textile',)),
        'painting':      ('paintings',     ('http://purl.org/NET/Claros/vocab#Ashmolean/Category/painting',)),
        'bound-volume':  ('bound volumes', ('http://purl.org/NET/Claros/vocab#Ashmolean/Category/bound_volume',)),

        'statuette':     ('statuettes',    ('http://arachne.uni-koeln.de/type/objectType/statuette',
                                            'http://purl.org/NET/Claros/vocab#LIMC/Support/statuette')),
        'mosaic':        ('mosaics',       ('http://arachne.uni-koeln.de/type/objectType/mosaik',
                                            'http://purl.org/NET/Claros/vocab#LIMC/Domaine/polychrome_mosaic')),
        'portrait':      ('portraits',     ('http://arachne.uni-koeln.de/type/objectType/portrait',)),
        'relief':        ('reliefs',       ('http://arachne.uni-koeln.de/type/objectType/relief',
                                            'http://purl.org/NET/Claros/vocab#LIMC/Domaine/relief')),
        'monument':      ('monuments',     ('http://arachne.uni-koeln.de/type/objectType/monument',)),

        'sculpture-in-the-round': ('sculpture in the round', ('http://purl.org/NET/Claros/vocab#LIMC/Domaine/sculpture_in_the_round',)),
        'gem':           ('gems',          ('http://purl.org/NET/Claros/vocab#LIMC/Domaine/gem',
                                            'http://arachne.uni-koeln.de/type/objectType/gemme',
                                            'http://arachne.uni-koeln.de/type/objectType/gemme-kameo')),

        'statue':        ('statues',       ('http://purl.org/NET/Claros/vocab#LIMC/Support/statue',)),
        'applique':      ('applique',      ('http://purl.org/NET/Claros/vocab#LIMC/Support/applique',)),
        'papyrus':       ('papyrus',       ('http://arachne.uni-koeln.de/type/objectType/papyrus',)),
    }

    @cached_view
    def handle_GET(self, request, context, ptype=None):
        context['types'] = sorted(self._OBJECT_TYPES.items(), key=lambda i:i[1][0])
        if ptype is None:
            return self.render(request, context, 'claros/objects-index')
        if ptype not in self._OBJECT_TYPES:
            raise Http404
        sub_queries = []
        for uri in self._OBJECT_TYPES[ptype][1]:
            sub_queries.append(self._sub_query % rdflib.URIRef(uri).n3())
        graph = self.endpoint.query(self._query % ' UNION '.join(sub_queries))
        subjects = set(graph.subjects(NS['crm'].P138i_has_representation))
        subjects = [Resource(s, graph, self.endpoint) for s in subjects]
        random.shuffle(subjects)
        subjects = subjects[:200]
        context.update({
            'graph': graph,
            'subjects': subjects,
            'query': graph.query,
            'type': self._OBJECT_TYPES[ptype],
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
            'query': results.query,
        })
        return self.render(request, context, 'claros/people')

class ForbiddenView(BaseView):
    @cached_view
    def handle_GET(self, request, context):
        context['status_code'] = 403
        return self.render(request, context, 'forbidden')
