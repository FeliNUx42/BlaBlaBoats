const bounds = {
  lat: document.querySelector("input#lat"),
  lng: document.querySelector("input#lng"),
  dist: document.querySelector("input#dist"),
  unit: document.querySelector("select#unit"),
  btn: document.querySelector("button#map-btn")
};

const dates = {
  start_date: document.querySelector("input#start_date"),
  end_date: document.querySelector("input#end_date")
}

const types = {
  boat_type: document.querySelector("select#boat_type"),
  sailing_mode: document.querySelector("select#sailing_mode"),
  people: document.querySelector("input#people")
}


function clearMap({ lat, lng, dist, unit, btn }) {
  lat.value = "";
  lng.value = "";
  dist.value = "";
  unit.value = "km";
  btn.innerHTML = "lat: -, lng: -";
}

function clearDate({ start_date, end_date }) {
  start_date.value = "";
  end_date.value = "";
}

function clearType({ boat_type, sailing_mode, people }) {
  boat_type.value = "All";
  sailing_mode.value = "All";
  people.value = "";
}