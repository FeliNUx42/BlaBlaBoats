var result_map;

const resultsMapElement = document.querySelector("#results");
const r_osm = L.tileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png");

const resultsDefaultLocation = { lat: 50, lng: 0 };
const resultsZoom = 6;

const results_bounds = L.latLngBounds();

// darkMode defined in ./dark_mode.js


function showResults() {
  if (result_map) return;
  if (typeof dest == "undefined") return;
  if (typeof trips == "undefined") return;

  result_map = L.map(resultsMapElement, {
    center: resultsDefaultLocation,
    zoom: resultsZoom
  });

  r_osm.addTo(result_map);

  if (dest.filtered) setFilteredMarkers();
  else setUnfilteredMarkers();

  setTimeout(() => {
    result_map.invalidateSize();
    result_map.fitBounds(results_bounds);
  }, 300);
}

function setFilteredMarkers() {
  let destinations = dest.dest;

  destinations.map(setMarker);

  destinations.map(d => results_bounds.extend(d.location));
}

function setUnfilteredMarkers() {
  let destinations = dest.dest;

  destinations.map(t => {
    t.map(setMarker);

    t.filter(d => d.location).map(d => results_bounds.extend(d.location));

    L.polyline(t.filter(d => d.location).map(d => d.location)).addTo(result_map);
  });
}

function setMarker(d) {
  if (!d.location) return;

  let {location, arrival, departure, trip_title, trip_url} = d;

  arrival = arrival ? arrival = moment(arrival).format("DD MMM") : "?";
  departure = departure ? departure = moment(departure).format("DD MMM") : "?";

  let link = `<i>${arrival}</i> to <i>${departure}</i>: <a href="${trip_url}">${trip_title}</a>`;

  L.marker(location).bindPopup(link).addTo(result_map);

  /*
    map: result_map,
    position: d.location,
    title: `${trips[d.trip_title]}: <a href="${d.trip_url}">${d.trip_title}</a>`,
    label: trips[d.trip_title],
    optimized: false
  });

  m.addListener("click", () => {
    infoWindow.close();
    infoWindow.setContent(m.getTitle());
    infoWindow.open(m.getMap(), m);
  });*/
}