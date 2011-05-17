function voyager_simple_map(id, longitude, latitude) {
	map = new OpenLayers.Map(id, { controls: [] });
    map.addLayer(new OpenLayers.Layer.OSM());
    map.addControl(new OpenLayers.Control.Navigation());
    map.addControl(new OpenLayers.Control.KeyboardDefaults());
    map.addControl(new OpenLayers.Control.Attribution("D"));
 
    var lonLat = new OpenLayers.LonLat(longitude, latitude)
          .transform(
            new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
            map.getProjectionObject() // to Spherical Mercator Projection
          );
 
    var zoom=4;
 
    var markers = new OpenLayers.Layer.Markers( "Markers" );
    map.addLayer(markers);
 
    markers.addMarker(new OpenLayers.Marker(lonLat));
 
    map.setCenter (lonLat, zoom);

}

$(function () {
	$('#query').css('overflow', 'hidden').css('cursor', 'pointer').height(150).append($('<div id="query-fade"/>').bind('click', expand_query)).bind('click', expand_query);
});
	
function expand_query() {
	$('#query-fade').remove();
	$('#query').css('height', 'auto').css('cursor', 'default').slideDown();
}