import rdflib

from django_conneg.views import HTMLView, JSONView
from humfrey.utils.views import EndpointView

from . import forms

class IndexView(HTMLView, JSONView, EndpointView):
    _json_indent = 2
    
    query = """\
        SELECT ?thing
               (SAMPLE(?literal_) AS ?literal)
               (SAMPLE(?score_) AS ?score)
               (SAMPLE(?label_) AS ?label)
               (SAMPLE(?depiction_) AS ?depiction) WHERE {
          {
            SELECT DISTINCT ?thing ?literal_ ?score_ WHERE {
              (?literal_ ?score_) pf:textMatch %s .
              ?thing ?x ?literal_
            } LIMIT 200
          } .
          OPTIONAL { ?thing rdfs:label ?label_ } .
          OPTIONAL { ?thing (crm:P138i_has_representation|^crm:P138_represents)+ ?depiction_ } .
          OPTIONAL { ?thing a crm:E38_Image . ?thing crm:empty{0} ?depiction_ } .
        } GROUP BY ?thing"""
        
    def simplify(self, value):
        if isinstance(value, rdflib.Literal):
            return unicode(value)
        elif isinstance(value, rdflib.URIRef):
            return unicode(value)
        elif isinstance(value, rdflib.BNode):
            return None
        else:
            return super(IndexView, self).simplify(value)
        
    def get(self, request):
        form = forms.SearchForm(request.GET or None)
        context = {'form': form,
                   'results': None,
                   'query': request.GET.get('query')}
        
        if form.is_valid():
            query = self.query % rdflib.Literal(form.cleaned_data['query']).n3()
            context['results'] = self.endpoint.query(query)
        
        return self.render(request, context, 'search/index')