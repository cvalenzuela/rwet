/*
Directions.
RWET 2017

cvalenzuela
*/

// Variables
var routes = [];
var instructions_set;

// Mapzen map
L.Mapzen.apiKey = "mapzen-u1JCMvx";
var map = L.Mapzen.map("map", {
  // center: [41.8758,-87.6189],
  zoom: 8
});

// Routing control
L.Routing.control({
  waypoints: [
    L.latLng(40.729603, -73.993704),
    L.latLng(40.729644, -73.997196)
  ],
  lineOptions: {
    styles: [ {color: "white", opacity: 0.8, weight: 12},
    {color: "#2676C6", opacity: 1, weight: 6}
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
  $.getJSON($SCRIPT_ROOT + '/_get_text', {
    'routes': JSON.stringify(routes),
  }, function(data) {
    console.log(data.result.length)
    instructions_set = data.result
  });

  // Change the instructions
  for(var i = 0; i < e.routes[0].instructions.length; i++){
    if (instructions_set != null){
      e.routes[0].instructions[i].instruction = instructions_set[i];
    }
  }

})
.addTo(map);
