const NEW_HTML = `
<div class="input-group mb-2">
  <div class=input-group-prepend>
    <span class=input-group-text>Stopover 1</span>
  </div>
  <input class="form-control" id="dest-1-place" maxlength="64" name="dest-1-place" onfocus="create_autocomplete(this)" placeholder="">
  <input id="dest-0-lat" name="dest-1-lat" type="number" hidden="">
  <input id="dest-0-lng" name="dest-1-lng" type="number" hidden="">
</div>
<div class=input-group>
  <div class=input-group-prepend>
    <span class=input-group-text>Date of arrival</span>
  </div>
  <input class=form-control id=dest-1-arr_date name=dest-1-arr_date type=date>
  <div class=input-group-prepend>
    <span class=input-group-text>Date of departure</span>
  </div>
  <input class=form-control id=dest-1-dep_date name=dest-1-dep_date type=date>
  <div class=input-group-append>
    <button class="btn btn-outline-secondary dropdown-toggle"type=button data-toggle=dropdown>Actions</button>
    <div class=dropdown-menu>
      <button class=dropdown-item type=button onclick=delete_stopover(this)>Delete this Stopover</button>
      <button class=dropdown-item type=button onclick=add_stopover(this)>Add Stopover below</button>
    </div>
  </div>
</div>`;


function add_stopover(addBtn) {
  // get the container and retreive index
  let container = addBtn.parentNode.parentNode.parentNode.parentNode;
  let index = Number(container.classList[0].split("-")[1]);

  // get list with all destinations
  let destinations = Array.from(container.parentNode.children)

  // only keep the ones after the clicked container
  destinations = destinations.filter(dest => {
    let num = dest.classList[0].split("-")[1];
    return Number(num) > index ? num : false;
  });

  // loop through all remaining destinations
  destinations.forEach((dest, i) => {
    // determin the current and new index of the container
    let num = index + i + 1;
    let new_num = num + 1;

    // rename the stopovers (Stopover 3 => Stopover 4)
    let prepend = dest.querySelector("span.input-group-text")
    if (prepend.innerText.startsWith("Stopover")) {
      prepend.innerText = "Stopover " + new_num;
    }

    // replace the class name (dest-3 => dest-4)
    dest.className = dest.className.replace("dest-" + num, "dest-" + new_num);

    // replace the name & id of all inputs within this container
    dest.querySelectorAll("input").forEach(inp => {
      inp.name = inp.name.replace("dest-" + num, "dest-" + new_num);
      inp.id = inp.id.replace("dest-" + num, "dest-" + new_num);
    });
  });

  // create a new container and set the classes
  let newObj = document.createElement("div");
  newObj.classList.add("dest-" + (index + 1));
  newObj.classList.add("mb-4");

  // hide the new container so we can use slideDown()
  newObj.setAttribute("style", "display:none;")

  // add new content and replace the text
  newObj.innerHTML = NEW_HTML;
  newObj.innerHTML = newObj.innerHTML.replaceAll("dest-1", "dest-" + (index + 1)).replace("Stopover 1", "Stopover " + (index + 1));

  // insert new container and make it visible
  container.parentNode.insertBefore(newObj, container.nextElementSibling);
  $(".dest-" + (index + 1)).slideDown();
}


function delete_stopover(delBtn) {
  // get the container and retreive index
  let container = delBtn.parentNode.parentNode.parentNode.parentNode;
  let index = Number(container.classList[0].split("-")[1]);

  // hide the container
  $("." + container.classList[0]).slideUp();

  // get list with all destinations
  let destinations = Array.from(container.parentNode.children)

  // only keep the ones after the clicked container
  destinations = destinations.filter(dest => {
    let num = dest.classList[0].split("-")[1];
    return Number(num) > index ? num : false;
  });

  destinations.forEach((dest, i) => {
    // determin the current and new index of the container
    let num = index + i + 1;
    let new_num = num - 1;

    // rename the stopovers (Stopover 4 => Stopover 3)
    let prepend = dest.querySelector("span.input-group-text")
    if (prepend.innerText.startsWith("Stopover")) {
      prepend.innerText = "Stopover " + new_num;
    }

    // replace the class name (dest-4 => dest-3)
    dest.className = dest.className.replace("dest-" + num, "dest-" + new_num);

    // replace the name & id of all inputs within this container
    dest.querySelectorAll("input").forEach(inp => {
      inp.name = inp.name.replace("dest-" + num, "dest-" + new_num);
      inp.id = inp.id.replace("dest-" + num, "dest-" + new_num);
    });
  });

  // delete thhe element after 1s
  window.setTimeout(() => { container.remove(); }, 1000);
}

