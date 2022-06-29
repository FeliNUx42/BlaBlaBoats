function create_autocomplete(i) {
  if (i.hasAttribute("setup")) return;

  i.setAttribute("setup", "");

  let autocomplete = new google.maps.places.Autocomplete(i, {
    types: ["(regions)"],
    fields: ["geometry", "formatted_address"]
  });

  autocomplete.input = i;
  autocomplete.lat = next = i.nextElementSibling;
  autocomplete.lng = next.nextElementSibling;
  autocomplete.values = { input: "", lat: "", lng: "" };

  autocomplete.addListener("place_changed", () => {
    let place = autocomplete.getPlace();

    if (!place.geometry) autocomplete.values = { input: "", lat: "", lng: "" };
    else {
      autocomplete.values = {
        input: autocomplete.input.value,
        lat: place.geometry.location.lat(),
        lng: place.geometry.location.lng()
      };
    }
    fill(autocomplete, autocomplete.values);
  });

  autocomplete.input.addEventListener("focusout", () => {
    setTimeout(() => {
      if (autocomplete.input.value == "") {
        autocomplete.values = { input: "", lat: "", lng: "" };
      }
      fill(autocomplete, autocomplete.values);

    }, 250);
  });
}

function fill(elem, { input, lat, lng }) {
  elem.input.value = input;
  elem.lat.value = lat;
  elem.lng.value = lng;
}