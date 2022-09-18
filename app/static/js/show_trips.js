var trips_map;
var poly;

const tripMapElement = document.querySelector("#destinations-modal #map");
const t_osm = L.tileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png");
const markerLayer = L.layerGroup();

const tripsTitle = document.querySelector("#destinations-modal .modal-title");
const tripsDefaultLocation = { lat: 50, lng: 0 };
const tripsZoom = 11;

// darkMode defined in ./dark_mode.js

createMap();


function createMap() {
  trips_map = L.map(tripMapElement, {
    center: tripsDefaultLocation,
    zoom: tripsZoom
  });

  t_osm.addTo(trips_map);
  markerLayer.addTo(trips_map)
}

function loadMap(index) {
  setTimeout(() => {
    _loadMap(index);
  }, 300);

  markerLayer.clearLayers() 

  let dest = trips[index];
  tripsTitle.innerHTML = dest[0].trip_title;

  dest.map(d => {
    let pos = d.location;
    if (!pos) return;

    L.marker(pos).addTo(markerLayer);
  });

  poly = L.polyline(dest.filter(d => d.location).map(d => d.location)).addTo(markerLayer);
}

function _loadMap(index) {
  trips_map.invalidateSize();
  trips_map.fitBounds(poly.getBounds());
}