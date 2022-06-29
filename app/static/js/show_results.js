var result_map;

const resultsMapElement = document.querySelector("#results");
const resultsDefaultLocation = { lat: 50, lng: 0 };
const defaultPathColor = "#FF0000";
const resultsZoom = 6;

const latlngbounds = new google.maps.LatLngBounds();
const infoWindow = new google.maps.InfoWindow();

function showResults() {
  if (result_map) return;
  if (typeof dest == "undefined") return;
  if (typeof trips == "undefined") return;

  createResultMap();

  if (dest.filtered) setFilteredMarkers();
  else setUnfilteredMarkers();

  setTimeout(() => {
    result_map.fitBounds(latlngbounds);
    result_map.setCenter(latlngbounds.getCenter());
  }, 300);
}

function createResultMap() {
  result_map = new google.maps.Map(resultsMapElement, {
    zoom: resultsZoom,
    center: resultsDefaultLocation,
    mapTypeControl: false,
    streetViewControl: false,
    rotateControl: false
  });
}

function setFilteredMarkers() {
  let destinations = dest.dest;

  destinations.map(setMarker);

  destinations.map(d => latlngbounds.extend(d.location));
}

function setUnfilteredMarkers() {
  let destinations = dest.dest;

  destinations.map(t => {
    t.map(setMarker);

    t.filter(d => d.location).map(d => latlngbounds.extend(d.location));
    
    let path = new google.maps.Polyline({
      path: t.filter(d => d.location).map(d => d.location),
      strokeColor: defaultPathColor,
      geodesic: true,
      strokeOpacity: 1.0,
      strokeWeight: 2,
    });

    path.setMap(result_map);
  });
}

function setMarker(d) {
  if (!d.location) return;

  let m = new google.maps.Marker({
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
  });
}