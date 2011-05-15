from rdflib import URIRef

from django.utils.safestring import mark_safe, SafeData

from humfrey.utils.namespaces import register as register_namespace
from humfrey.utils.resource import register, Image

register(Image, 'crm:E38_Image')

class Place(object):
    @property
    def label(self):
        identifiers = self.get_all('crm:P87_is_identified_by')
        for identifier in identifiers:
        	if identifier.rdf_value:
        		return identifier.rdf_value
		
    def _augment(self):
    	if isinstance(self._identifier, URIRef):
    	    return self._endpoint.query("DESCRIBE ?x WHERE { { %(s)s claros:coordinates ?x } UNION { %(s)s crm:P87_is_identified_by ?x } }" % {'s': self._identifier.n3()})
        else:
            return []
            
    @property
    def spatial_coordinates(self): pass

    @property
    def geo_long(self):
    	return self.get('claros:coordinates').claros_has_geoObject.geo_long
    @property
    def geo_lat(self):
    	return self.get('claros:coordinates').claros_has_geoObject.geo_lat
        
register(Place, 'crm:E53_Place')

class PlaceName(object):
    @property
    def label(self):
        return self.rdf_value
register(PlaceName, 'crm:E48_Place_Name')

class SpatialCoordinates(object):
    @property
    def label(self):
        print self.claros_has_geoObject
        return "%s, %s" % (self.claros_has_geoObject.geo_lat, self.claros_has_geoObject.geo_long)
register(SpatialCoordinates, 'crm:E47_Place_Spatial_Coordinates')

class ManMadeObject(object):
    @property
    def geo_long(self):
        return self.crm_P16i_was_used_for.P7_took_place_at.geo_long
    @property
    def geo_lat(self):
        return self.crm_P16i_was_used_for.P7_took_place_at.geo_lat
          
    @classmethod
    def _describe_patterns(cls, uri, get_names):
    	print "ER"
        name, = get_names(1)
        params = {'uri': uri.n3(), 'name': name}
        return [
            '%(uri)s crm:P16i_was_used_for %(name)s' % params,
            '%(uri)s crm:P2_has_type %(name)s' % params,
            '%(uri)s crm:P138i_has_representation %(name)s' % params,
        ]
        
register(ManMadeObject, 'crm:E22_Man-Made_Object')

class Activity(object):
    def render(self):
        return mark_safe(u"Found at %s" % self.crm_P7_took_place_at.render())
    @property
    def label(self):
    	return 'e'
register(Activity, 'crm:E7_Activity')