from rdflib import URIRef

from django.utils.safestring import mark_safe, SafeData

from humfrey.utils.namespaces import register as register_namespace
from humfrey.utils.resource import register, Image

register(Image, 'crm:E38_Image')

class Place(object):
    @classmethod
    def _describe_patterns(cls, uri, get_names):
        name, = get_names(1)
        params = {'uri': uri.n3(), 'name': name}
        return [
            '%(uri)s crm:P87_is_identified_by %(name)s' % params,
            '%(uri)s claros:coordinates %(name)s' % params,
        ]

    @property
    def spatial_coordinates(self): pass

    @property
    def geo_long(self):
        return self.get('claros:coordinates').geo_long
    @property
    def geo_lat(self):
        return self.get('claros:coordinates').geo_lat

register(Place, 'crm:E53_Place')

class PlaceName(object):
    @property
    def label(self):
        return self.rdf_value
register(PlaceName, 'crm:E48_Place_Name')

class SpatialCoordinates(object):
    @property
    def label(self):
        return "%s, %s" % (self.claros_has_geoObject.geo_lat, self.claros_has_geoObject.geo_long)

    def geo_lat(self):
        return self.get('claros:has_geoObject').geo_lat

    def geo_long(self):
        return self.get('claros:has_geoObject').geo_long

register(SpatialCoordinates, 'crm:E47_Place_Spatial_Coordinates')

class Point(object):
    @property
    def label(self):
        return "POINT(%s, %s)" % (self.geo_lat, self.geo_long)
register(Point, 'geo:Point')

class Birth(object):
    @property
    def label(self):
        ts = self.get('crm:P4_has_time-span')
        return mark_safe('%s, at %s' % (ts.rdfs_label, self.crm_P7_took_place_at.render()))
register(Birth, 'crm:E67_Birth')

class ManMadeObject(object):
    @property
    def geo_long(self):
        find_coordinates = self.get('claros:coordinates-find')
        return find_coordinates.geo_long if find_coordinates else None
    @property
    def geo_lat(self):
        find_coordinates = self.get('claros:coordinates-find')
        return find_coordinates.geo_lat if find_coordinates else None
    @classmethod
    def _describe_patterns(cls, uri, get_names):
        name, = get_names(1)
        params = {'uri': uri.n3(), 'name': name}
        return [
            '%(uri)s claros:coordinates-find %(name)s' % params,
            '%(uri)s crm:P16i_was_used_for %(name)s' % params,
            '%(uri)s crm:P2_has_type %(name)s' % params,
            '%(uri)s crm:P138i_has_representation %(name)s' % params,
        ]
register(ManMadeObject, 'crm:E22_Man-Made_Object')

class Activity(object):
    def render(self):
        return mark_safe(u"Found at %s" % self.crm_P7_took_place_at.render())
#    @property
#    def label(self):
#        return 'e'
register(Activity, 'crm:E7_Activity')


class Person(object):
    @classmethod
    def _describe_patterns(cls, uri, get_names):
        n1, n2 = get_names(2)
        params = {'uri': uri.n3(), 'n1': n1, 'n2': n2}
        return [
            '%(uri)s claros:coordinates-born %(n1)s' % params,
            '%(uri)s crm:P98i_was_born %(n1)s . %(n1)s crm:P7_took_place_at %(n2)s' % params,
            '%(uri)s crm:P131_is_identified_by %(n1)s' % params,
        ]
register(Person, 'crm:E21_Person')

class ActorAppellation(object):
    @property
    def label(self):
        value = self.rdf_value
        return '%s (%s)' % (unicode(value), value.language)
register(ActorAppellation, 'crm:E82_Actor_Appellation')
