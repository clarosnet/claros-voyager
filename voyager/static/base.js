var sparqlEndpoint = "http://data.clarosnet.org/sparql/";
var descURL = "http://data.clarosnet.org/desc/?uri=";
var thumbnailURL = "/thumbnail/";

function query(query, func) {
	$.post(sparqlEndpoint, {
		'query': query,
		'format': 'srj',
		'common_prefixes': 'on',
	}, function(data) { func(data.head.vars, data.results.bindings)}, 'json');
}

function voyager_simple_map(id, longitude, latitude) {
	var latLng = new google.maps.LatLng(latitude, longitude);
	var options = {
		center: latLng,
		zoom: 8,
		mapTypeId: google.maps.MapTypeId.TERRAIN
	};
	var map = new google.maps.Map(document.getElementById(id), options);
	var marker = new google.maps.Marker({
		position: latLng,
		map: map,
	});
};

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
	var options = {
		center: new google.maps.LatLng(0, 0),
		zoom: 2,
		mapTypeId: google.maps.MapTypeId.TERRAIN
	};
	var map = new google.maps.Map(document.getElementById("places-map"), options);

	query(placesQuery, function(vars, bindings) {
	
		var size = new google.maps.Size(12, 15);
		var origin = new google.maps.Point(6, 15);
		var icon = new google.maps.MarkerImage('http://www.beazley.ox.ac.uk/XDB/images/icoClarosMarker.png', size, origin);

		for (var i in bindings) {
			var binding = bindings[i];
			var latLng = new google.maps.LatLng(binding.lat.value, binding.long.value);
			var marker = new google.maps.Marker({
				//icon: icon,
				position: latLng,
				map: map,
				title: binding.label.value,
				icon: 'http://www.beazley.ox.ac.uk/XDB/images/icoClarosMarker.png',
			});
			google.maps.event.addListener(marker, 'click', showPlace(map, latLng, binding));
		}
	})
}

function showPlace(map, lonLat, binding) { return function(evt) {
  var smallThumbnailURL = thumbnailURL + "?width=50&height=50&url=";
	
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
      var li = $("<li/>");
      if (binding.image)
        li.css('background-image', "url('" + smallThumbnailURL + encodeURIComponent(binding.image.value) + "')");
      li.append($('<a/>').attr('href', descURL + encodeURI(binding.thing.value)).text(binding.label.value));
      ul.append(li);
    }
  });
};}
