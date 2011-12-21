var sparqlEndpoint = "http://data.clarosnet.org/sparql/";
var descURL = "http://data.clarosnet.org/desc/?uri=";

function query(query, func) {
	$.post(sparqlEndpoint, {
		'query': query,
		'format': 'srj',
		'common_prefixes': 'on',
	}, function(data) { func(data.head.vars, data.results.bindings)}, 'json');
}

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
	if ($('#query').height() > 150) 
	    $('#query').css('overflow', 'hidden').css('cursor', 'pointer').height(150).append($('<div id="query-fade"/>').bind('click', expand_query)).bind('click', expand_query);
});
	
function expand_query() {
	$('#query-fade').remove();
	$('#query').css('height', 'auto').css('cursor', 'default').slideDown();
}

var placesQuery = ["SELECT ?place (SAMPLE(?lat_) as ?lat) (SAMPLE(?long_) as ?long) (SAMPLE(?label_) as ?label) WHERE {",
                   "  { SELECT ?place ?coords WHERE { ?place crm:P87_is_identified_by ?coords . ?coords a crm:E47_Place_Spatial_Coordinates . FILTER(EXISTS { ?thing claros:coordinates-find ?coords } ) } } .",
                   "  ?place",
                   "    rdfs:label ?label_ ;",
                   "    geo:long ?long_ ;",
                   "    geo:lat ?lat_ ;",
                   "    a crm:E53_Place .",
                   "  FILTER(EXISTS { ?thing claros:coordinates-find ?coords } )",
                   //"    crm:P2_has_type <http://id.clarosnet.org/type/place/country> ;",
                   "} GROUP BY ?place"
                  ].join('\n');

var placeDetailQuery = ["SELECT ?thing (SAMPLE(?image_) as ?image) (SAMPLE(?label_) as ?label) {",
                        "  <PLACE> claros:coordinates ?coords .",
                        "  ?thing claros:coordinates-find ?coords ;",
                        "    rdfs:label ?label_ .",
                        "  OPTIONAL {",
                        "    ?thing crm:P138i_has_representation ?image_",
                        "  }",
                        "} GROUP BY ?thing ORDER BY ?label"
                       ].join('\n');


function initPlaces() {
  query(placesQuery, function(vars, bindings) {
	map = new OpenLayers.Map("places-map", {});
    map.addLayer(new OpenLayers.Layer.OSM());
	
    var lonLat = new OpenLayers.LonLat(0,0)
    .transform(
      new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
      map.getProjectionObject() // to Spherical Mercator Projection
    );

    var markers = new OpenLayers.Layer.Markers( "Markers" );
    map.addLayer(markers);
    

    var size = new OpenLayers.Size(13,22);
    var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
    var icon = new OpenLayers.Icon('/site-media/marker.png',size,offset);
    
    
    for (var i in bindings) {
      var binding = bindings[i];
      lonLat = new OpenLayers.LonLat(binding.long.value, binding.lat.value).transform(
                 new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
                 map.getProjectionObject() // to Spherical Mercator Projection
               );
      marker = new OpenLayers.Marker(lonLat, icon.clone());
      marker.events.register('mousedown', marker, showPlace(map, lonLat, binding));
      markers.addMarker(marker);
    }
    
	map.setCenter(lonLat, 2);
  })
}

function showPlace(map, lonLat, binding) { return function(evt) {
  var thumbnailURL = "/external-image/?width=50&height=50&url=";
	
  var div = $('#places-map');
  var ul = $('<ul/>').addClass('placeDetailObjects');
  var detailInner = $('<div/>');
  var center = map.getCenter();
  div.width(div.parent().width()-400);
  map.setCenter(center);
  detailInner
      .css('padding-left', '10px')
      .css('padding-right', '10px')
      .css('padding-bottom', '10px')
      .append($('<h2/>').text(binding.label.value).css('margin-top', '0'))
      .append($('<a/>').attr('href', descURL + encodeURI(binding.place.value)).text(binding.place.value))
      .append(ul);

  $('#place-detail').css('display', 'block').empty().append(detailInner);
  
  query(placeDetailQuery.replace("PLACE", binding.place.value), function(vars, bindings) {
    for (var i in bindings) {
      var binding = bindings[i];
      var li = $("<li/>").css('clear', 'left');
      if (binding.image)
    	li.append($('<div/>').css('height', '50px').css('width', '50px').css('align', 'center').css('float', 'left')
                             .append($('<a/>').attr('href', descURL + encodeURI(binding.thing.value))
                                              .append($('<img/>').attr('src', thumbnailURL + encodeURI(binding.image.value)))));
      li.append($('<div/>').addClass('placeDetailObjectLabel')
    		               .append($('<a/>').attr('href', descURL + encodeURI(binding.thing.value)).text(binding.label.value)));
      ul.append(li);
    }
  });
};}
