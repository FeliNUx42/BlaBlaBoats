var map;

const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

const mapElement = document.querySelector("#map-modal #map");
const title = document.querySelector("#map-modal .modal-title");
const defaultLocation = { lat: 50, lng: 0 };
const defaultPathColor = "#FF0000";
const zoom = 6;

// darkMode defined in ./dark_mode.js


function createMap() {
  map = new google.maps.Map(mapElement, {
    mapId: MAP_IDS.at(darkMode),
    zoom: zoom,
    center: defaultLocation,
    mapTypeControl: false,
    streetViewControl: false,
    rotateControl: false
  });

  destinations.map((dest, i) => {
    let pos = dest.location;
    if (!pos) return;

    new google.maps.Marker({
      map: map,
      position: pos,
      label: labels[i % labels.length]
    });
  });

  let path = new google.maps.Polyline({
    path: destinations.filter(d => d.location).map(d => d.location),
    geodesic: true,
    strokeColor: defaultPathColor,
    strokeOpacity: 1.0,
    strokeWeight: 2,
  });

  path.setMap(map);
}

function loadMap(index) {
  if (!map) createMap();

  let { name, location, arrival, departure, trip_title, trip_url } = destinations[index];

  arrival = arrival ? arrival = moment(arrival).format("DD MMM") : "?";
  departure = departure ? departure = moment(departure).format("DD MMM") : "?";

  title.innerHTML = `${name} ( <i>${arrival}</i> to <i>${departure}</i> )`;

  map.setCenter(location);
  map.setZoom(zoom);
}