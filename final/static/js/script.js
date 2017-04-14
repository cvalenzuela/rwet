/*
Directions.
RWET 2017

cvalenzuela
*/

// Variables
var routes;
var test_text;

// Mapzen map
L.Mapzen.apiKey = "mapzen-u1JCMvx";
var map = L.Mapzen.map("map", {
  // center: [41.8758,-87.6189],
  zoom: 16
});

// Routing control
L.Routing.control({
  waypoints: [
    L.latLng(40.7828687,-73.9675438),
    L.latLng(40.7294285,-73.9958957)
  ],
  lineOptions: {
    styles: [ {color: "white", opacity: 0.8, weight: 12},
    {color: "#2676C6", opacity: 1, weight: 6}
  ]},
  router: L.Routing.mapzen("mapzen-u1JCMvx", {costing:"auto"}),
  formatter: new L.Routing.mapzenFormatter(),
  summaryTemplate:'<div class="start">{name}</div><div class="info {costing}">{distance}, {time}</div>',
  routeWhileDragging: false,
  geocoder: L.Control.Geocoder.nominatim()
})
.on('routesfound', function(e) {
  routes = e.routes;

  $.getJSON($SCRIPT_ROOT + '/_get_text', {
    'lat': 3,
    'lng': 2,
    'length': routes[0]["instructions"].length
  }, function(data) {
    test_text = data.result
    console.log(data)
    // $("#result").text(data.result);
  });

  for(var i = 0; i < routes[0]["instructions"].length; i++){
    if (test_text != null){
      e.routes[0]["instructions"][i].instruction = test_text[Math.floor(Math.random() * test_text.length)];
      console.log(e.routes[0]["instructions"][i].instruction);
    }
  }

})
.addTo(map);
