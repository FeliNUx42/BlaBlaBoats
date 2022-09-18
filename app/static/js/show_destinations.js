var map;
var poly;

const mapElement = document.querySelector("#map-modal #map");
const osm = L.tileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png");

const title = document.querySelector("#map-modal .modal-title");
const defaultLocation = { lat: 50, lng: 0 };
const zoom = 11;

// darkMode defined in ./dark_mode.js


function createMap() {
  map = L.map(mapElement, {
    center:defaultLocation,
    zoom:zoom
  });

  osm.addTo(map);

  destinations.map((dest, i) => {
    let pos = dest.location;
    if (!pos) return;

    L.marker(pos).addTo(map);
  });
  
  poly = L.polyline(destinations.filter(d => d.location).map(d => d.location)).addTo(map);
}

function loadMap(index) {
  setTimeout(() => {
    _loadMap(index);
  }, 300);
}

function _loadMap(index) {
  map.invalidateSize();

  if (index < 0) {
    map.fitBounds(poly.getBounds());
    return;
  }

  let { name, location, arrival, departure } = destinations[index];

  arrival = arrival ? arrival = moment(arrival).format("DD MMM") : "?";
  departure = departure ? departure = moment(departure).format("DD MMM") : "?";

  title.innerHTML = `${name} ( <i>${arrival}</i> to <i>${departure}</i> )`;

  map.setView(location, zoom);
}