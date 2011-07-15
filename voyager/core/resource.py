from rdflib import URIRef

from django.utils.safestring import mark_safe, SafeData

from humfrey.utils.namespaces import register as register_namespace
from humfrey.utils.resource import register, Image

register(Image, 'crm:E38_Image')

class Place(object):
    @classmethod
    def _describe_patterns(cls):
        return [
            '%(uri)s crm:P87_is_identified_by %(place_identifier)s',
            '%(uri)s claros:coordinates %(place_coordinates)s',
        ]

    @property
    def spatial_coordinates(self): pass

    @property
    def geo_long(self):
        ids = self.get_all('crm:P87_is_identified_by')
        for id_ in ids:
            if id_.geo_long:
               return id_.geo_long
    @property
    def geo_lat(self):
        ids = self.get_all('crm:P87_is_identified_by')
        for id_ in ids:
            if id_.geo_lat:
               return id_.geo_lat

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
    def render(self):
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
    def _describe_patterns(cls):
        return [
            '%(uri)s claros:coordinates-find %(coordinates_find)s',
            '%(uri)s crm:P16i_was_used_for %(object_use)s',
            '%(uri)s crm:P2_has_type %(object_type)s',
            '%(uri)s crm:P138i_has_representation %(object_representation)s',
        ]
register(ManMadeObject, 'crm:E22_Man-Made_Object')

class Activity(object):
    def render(self):
        try:
            return mark_safe(u"Found at %s" % self.crm_P7_took_place_at.render())
        except AttributeError:
            return "Undescribed find event"

#    @property
#    def label(self):
#        return 'e'
register(Activity, 'crm:E7_Activity')


class Person(object):
    @classmethod
    def _describe_patterns(cls):
        return [
            '%(uri)s claros:coordinates-born %(n1)s',
            '%(uri)s crm:P98i_was_born %(n1)s . %(n1)s crm:P7_took_place_at %(n2)s ; crm:P4_has_time-span %(n3)s',
            '%(uri)s crm:P131_is_identified_by %(n1)s',
        ]
register(Person, 'crm:E21_Person')

class ActorAppellation(object):
    @property
    def label(self):
        value = self.rdf_value
        return '%s (%s)' % (unicode(value), value.language)
register(ActorAppellation, 'crm:E82_Actor_Appellation')
