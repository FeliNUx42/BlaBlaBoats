var map;
var circle;

const M_TO_KM = 1000;
const M_TO_MI = 1609.344;
const M_TO_NMI = 1852;

const filterMapElement = document.querySelector("#map-modal #map");
const filterDefaultLocation = { lat: 50, lng: 0 };
const filterZoom = 6;

const circleColor = "#343a40";
const defaultRadius = 150 * M_TO_KM;
const maxRadius = 3000 * M_TO_KM;

// bounds defined in ./clear_filters.js
// darkMode defined in ./dark_mode.js


function openFilterMap({ dist, unit }) {
  if (!map) createFilterMap();
  if (!circle) createFilterCircle();

  let r = 0;

  if (unit.value == "km") r = Number(dist.value) * M_TO_KM;
  if (unit.value == "mi") r = Number(dist.value) * M_TO_MI;
  if (unit.value == "nmi") r = Number(dist.value) * M_TO_NMI;

  if (r != 0) circle.setRadius(r)
}

function createFilterMap() {
  navigator.geolocation.getCurrentPosition(centerMap)

  map = new google.maps.Map(filterMapElement, {
    mapId: MAP_IDS.at(darkMode),
    zoom: filterZoom,
    center: filterDefaultLocation,
    mapTypeControl: false,
    streetViewControl: false,
    rotateControl: false
  });
}

function createFilterCircle() {
  circle = new google.maps.Circle({
    strokeColor: circleColor,
    strokeOpacity: 0.8,
    strokeWeight: 1,
    fillColor: circleColor,
    fillOpacity: 0.3,
    center: { lat: map.center.lat(), lng: map.center.lng() },
    radius: defaultRadius,
    editable: true,
    draggable: true
  });

  circle.setMap(map);

  circle.addListener("bounds_changed", () => {
    if (circle.radius > maxRadius) circle.setRadius(maxRadius);
  });
}

function centerMap(location) {
  pos = {
    lat: location.coords.latitude,
    lng: location.coords.longitude
  }

  map.setCenter(pos);
  circle.setCenter(pos);
}

function setBoundaries({ lat, lng, dist, unit, btn }) {
  let r = circle.getRadius();

  if (unit.value == "km") r /= M_TO_KM;
  if (unit.value == "mi") r /= M_TO_MI;
  if (unit.value == "nmi") r /= M_TO_NMI;

  dist.value = r.toFixed();

  lat.value = _lat = circle.center.lat();
  lng.value = _lng = circle.center.lng();

  btn.innerHTML = `lat: ${_lat.toFixed(2)}, lng: ${_lng.toFixed(2)}`;
}