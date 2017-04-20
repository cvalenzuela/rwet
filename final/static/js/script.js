/*
Directions.
RWET 2017

cvalenzuela
*/

// Variables
var routes = [];
var instructions_set;

var originalRoutes;

var loading = document.getElementById('loading');

// Mapzen map
L.Mapzen.apiKey = "mapzen-u1JCMvx";
var map = L.Mapzen.map("map", {
  // center: [41.8758,-87.6189],
  zoom: 8,
  dragging: false,
  maxZoom: 18,
  zoomControl: false,
  // trackResize: false,
  // boxZoom: false,
  // doubleClickZoom: false,
  // attributionControl: false,
  scrollWheelZoom: false
});

// var map = L.map('map');
//
// var layer = Tangram.leafletLayer({
//     scene: 'static/js/scene.yaml',
//     attribution: '<a href="https://mapzen.com/tangram" target="_blank">Tangram</a> | &copy; OSM contributors | <a href="https://mapzen.com/" target="_blank">Mapzen</a>'
// });

// layer.addTo(map);

// map.setView([40.70531887544228, -74.00976419448853], 9);

var imageIcon = L.icon({
  iconUrl: 'static/js/images/icon.png',
  shadowUrl: 'static/js/images/iconshadow.png',

  iconSize:     [0, 0], // size of the icon
  shadowSize:   [0, 0], // size of the shadow
  iconAnchor:   [0, 0], // point of the icon which will correspond to marker's location
  shadowAnchor: [1, 1],  // the same for the shadow
  popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
});

// Routing control
var routeControls = L.Routing.control({
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
    {color: "#aaaaaa", opacity: 0.8, weight: 12},
    {color: "#aaaaaa", opacity: 1, weight: 6}
    ]},
  router: L.Routing.mapzen("mapzen-u1JCMvx", {costing:"pedestrian"}),
  formatter: new L.Routing.mapzenFormatter(),
  summaryTemplate:'<div class="start">{name}</div><div class="info {costing}">{distance}, {time}</div>',
  routeWhileDragging: false,
  geocoder: L.Control.Geocoder.nominatim(),
})

.on('routesfound', function(e) {
  originalRoutes = e;
  routes = [];
  console.log('1) Amount of found routes for this two addresses: ' + originalRoutes.routes[0].instructions.length);
  loading.style.display = 'block'
  // store every waypoint instruction, lat and lng
  for (var i = 0; i < originalRoutes.routes[0].instructions.length; i++){
    var route = {
      "lat": originalRoutes.routes[0].coordinates[originalRoutes.routes[0].instructions[i].index][0],
      "lng": originalRoutes.routes[0].coordinates[originalRoutes.routes[0].instructions[i].index][1],
      "instruction": originalRoutes.routes[0].instructions[i].instruction.toLowerCase()
    }
    routes.push(route);
  }

  // Change the instructions
  function changeInstructions(){
    var td = document.getElementsByTagName('td')
    var current = 0;

    // get all current instructions and change them
    for(var i = 0; i <td.length; i++){
      if(td[i].innerText.length > 10){
        console.log('3.' + i + ') Changing route: ' + td[i].innerText +  ' -- with: ' + instructions_set[current] )
        td[i].innerText = instructions_set[current]
        current ++;
      }
    }
  }

  // Send the data AJAX to server
  $.getJSON($SCRIPT_ROOT + '/_lstm', {
    'routes': JSON.stringify(routes),
  }, function(data) {
    instructions_set = []
    instructions_set = data.result
    //console.log(data.status)
    console.log('2) The server responded with a set of instruction of: ' + instructions_set.length)
    changeInstructions()
    loading.style.display = 'none'
  });
})
.addTo(map);
