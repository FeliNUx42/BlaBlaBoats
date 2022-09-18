var map;
var circle;
var last_pos;

const M_TO_KM = 1000;
const M_TO_MI = 1609.344;
const M_TO_NMI = 1852;

const filterMapElement = document.querySelector("#map-modal #map");
const filterOsm = L.tileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png");

const filterDefaultLocation = { lat: 50, lng: 0 };
const filterZoom = 6;

const defaultRadius = 150 * M_TO_KM;

// bounds defined in ./clear_filters.js
// darkMode defined in ./dark_mode.js


function openFilterMap({ dist, unit }) {
  if (!map) createFilterMap();
  if (!circle) createFilterCircle();

  setTimeout(() => {
    map.invalidateSize();
  }, 300);

  circle.disableEdit();
  circle.setLatLng({...last_pos});
  circle.enableEdit();
  let r = 0;

  if (unit.value == "km") r = Number(dist.value) * M_TO_KM;
  if (unit.value == "mi") r = Number(dist.value) * M_TO_MI;
  if (unit.value == "nmi") r = Number(dist.value) * M_TO_NMI;

  if (r != 0) circle.setRadius(r)
}

function createFilterMap() {
  map = L.map(filterMapElement, {
    editable: true,
    center: filterDefaultLocation,
    zoom: filterZoom
  });

  filterOsm.addTo(map);
}

function createFilterCircle() {
  circle = L.circle(map.getCenter(), {radius: defaultRadius});
  circle.addTo(map);
  circle.enableEdit();

  last_pos = {...circle.getLatLng()};
}

function setBoundaries({ lat, lng, dist, unit, btn }) {
  let r = circle.getRadius();

  if (unit.value == "km") r /= M_TO_KM;
  if (unit.value == "mi") r /= M_TO_MI;
  if (unit.value == "nmi") r /= M_TO_NMI;

  dist.value = r.toFixed();

  let pos = circle.getLatLng();
  last_pos = {...pos}

  lat.value = pos.lat;
  lng.value = pos.lng;

  btn.innerHTML = `lat: ${pos.lat.toFixed(2)}, lng: ${pos.lng.toFixed(2)}`;
}