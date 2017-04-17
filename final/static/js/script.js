/*
Directions.
RWET 2017

cvalenzuela
*/

// Variables
var routes = [];
var instructions_set;

// Mapzen map
// L.Mapzen.apiKey = "mapzen-u1JCMvx";
// var map = L.Mapzen.map("map", {
//   // center: [41.8758,-87.6189],
//   zoom: 8
// });

var map = L.map('map');

var layer = Tangram.leafletLayer({
    scene: 'static/js/scene.yaml',
    attribution: '<a href="https://mapzen.com/tangram" target="_blank">Tangram</a> | &copy; OSM contributors | <a href="https://mapzen.com/" target="_blank">Mapzen</a>'
});

layer.addTo(map);

// map.setView([40.70531887544228, -74.00976419448853], 9);

var imageIcon = L.icon({
  iconUrl: 'static/js/images/hatch_2.png',
  iconSize:     [38, 45], // size of the icon
  iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
});

// Routing control
L.Routing.control({
  waypoints: [
    L.latLng(40.729603, -73.993704),
    L.latLng(40.729644, -73.997196)
  ],
  pointMarkerStyle: {
    radius: 5,color: '#000000',fillColor: 'white',opacity: 1,fillOpacity: 0.7
  },
  createMarker: function(i, waypoint, n){
    return L.marker(waypoint.latLng, {
      draggable: true,
      icon: imageIcon
    })
  },
  lineOptions: {
    styles: [
    {color: "#ffffff", opacity: 0.8, weight: 12},
    {color: "#ffffff", opacity: 1, weight: 6}
    ]},
  router: L.Routing.mapzen("mapzen-u1JCMvx", {costing:"pedestrian"}),
  formatter: new L.Routing.mapzenFormatter(),
  summaryTemplate:'<div class="start">{name}</div><div class="info {costing}">{distance}, {time}</div>',
  routeWhileDragging: false,
  geocoder: L.Control.Geocoder.nominatim()
})

.on('routesfound', function(e) {
  routes = [];

  // store every waypoint instruction, lat and lng
  for (var i = 0; i < e.routes[0].instructions.length; i++){
    var route = {
      "lat": e.routes[0].coordinates[e.routes[0].instructions[i].index][0],
      "lng": e.routes[0].coordinates[e.routes[0].instructions[i].index][1],
      "instruction": e.routes[0].instructions[i].instruction
    }
    routes.push(route);
  }

  // Send the data AJAX to server
  $.getJSON($SCRIPT_ROOT + '/_lstm', {
    'routes': JSON.stringify(routes),
  }, function(data) {
    instructions_set = data.result
    console.log(data.status)
    console.log(instructions_set)
  });

  // Change the instructions
  for(var i = 0; i < e.routes[0].instructions.length; i++){
    if (instructions_set != null){
      e.routes[0].instructions[i].instruction = instructions_set[i];
    }
  }

})
.addTo(map);
