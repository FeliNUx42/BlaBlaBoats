$(document).ready(function(){
  $('[data-toggle="popover"]').popover();

  var url = document.location.toString();
  if (url.match('#')) {
      $('.nav-tabs a[href="#' + url.split('#')[1] + '"]').tab('show');
  }
});

$(".custom-file-input").on("change", function() {
  var fileName = $(this).val().split("\\").pop();
  $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});

function delete_stopover(delBtn) {
  let obj = delBtn.parentNode.parentNode.parentNode.parentNode;
  let index = Number(obj.classList[0].split("-")[1]);

  $("."+obj.classList[0]).slideUp();

  let children = Array.from(obj.parentNode.children).filter(elem => {
    let num = elem.classList[0].split("-")[1];
    if (!num) return false;
    return Number(num) > index;
  });

  children.forEach((item, i) => {
    let num = index + i + 1;
    if (item.querySelector("span.input-group-text").innerText.startsWith("Stopover")) {
      item.querySelector("span.input-group-text").innerText = "Stopover " + (num-1);
    }
    item.className = item.className.replace("dest-"+num, "dest-"+(num-1));
    item.querySelectorAll("input").forEach(inp => {
      inp.name = inp.name.replace("dest-"+num, "dest-"+(num-1));
      inp.id = inp.id.replace("dest-"+num, "dest-"+(num-1));
    });
  });

  window.setTimeout(()=>{obj.remove();}, 1000);
}

function add_stopover(addBtn) {
  let obj = addBtn.parentNode.parentNode.parentNode.parentNode;
  let index = Number(obj.classList[0].split("-")[1]);

  let children = Array.from(obj.parentNode.children).filter(elem => {
    let num = elem.classList[0].split("-")[1];
    if (!num) return false;
    return Number(num) > index;
  });

  children.forEach((item, i) => {
    let num = index + i + 1;
    if (item.querySelector("span.input-group-text").innerText.startsWith("Stopover")) {
      item.querySelector("span.input-group-text").innerText = "Stopover " + (num+1);
    }
    item.className = item.className.replace("dest-"+num, "dest-"+(num+1));
    item.querySelectorAll("input").forEach(inp => {
      inp.name = inp.name.replace("dest-"+num, "dest-"+(num+1));
      inp.id = inp.id.replace("dest-"+num, "dest-"+(num+1));
    });
  });

  let newObj = document.createElement("div");
  newObj.classList.add("dest-"+(index+1));
  newObj.classList.add("mb-4");
  newObj.setAttribute("style", "display:none;")
  newObj.innerHTML = `<div class="input-group mb-2"><div class=input-group-prepend><span class=input-group-text>Stopover 1</span></div><input class="form-control" id="dest-1-place" maxlength="64" name="dest-1-place" onfocus="create_autocomplete(this)" placeholder=""><input id="dest-0-lat" name="dest-1-lat" type="number" hidden=""><input id="dest-0-lng" name="dest-1-lng" type="number" hidden=""></div><div class=input-group><div class=input-group-prepend><span class=input-group-text>Date of arrival</span></div><input class=form-control id=dest-1-arr_date name=dest-1-arr_date type=date><div class=input-group-prepend><span class=input-group-text>Date of departure</span></div><input class=form-control id=dest-1-dep_date name=dest-1-dep_date type=date><div class=input-group-append><button class="btn btn-outline-secondary dropdown-toggle"type=button data-toggle=dropdown>Actions</button><div class=dropdown-menu><button class=dropdown-item type=button onclick=delete_stopover(this)>Delete this Stopover</button> <button class=dropdown-item type=button onclick=add_stopover(this)>Add Stopover below</button></div></div></div>`;
  newObj.innerHTML = newObj.innerHTML.replaceAll("dest-1", "dest-"+(index+1)).replace("Stopover 1", "Stopover "+Number(index+1));

  obj.parentNode.insertBefore(newObj, obj.nextElementSibling);
  $(".dest-"+(index+1)).slideDown();
}

$(document).ready(function(){
  $(".collapse").on("show.bs.collapse", function () {
    $(`h3[data-target='#${this.id}'] .lni-circle-plus`).hide();
    $(`h3[data-target='#${this.id}'] .lni-circle-minus`).show();
  });

  $(".collapse").on("hide.bs.collapse", function () {
    $(`h3[data-target='#${this.id}'] .lni-circle-plus`).show();
    $(`h3[data-target='#${this.id}'] .lni-circle-minus`).hide();
  });
});

$("*[max-length]").each(function() {
  let max = Number($(this).attr("max-length"));
  if ($(this).html().length > max ) {
    $(this).html($(this).html().substr(0, max)+"...")
  }
});

function select_value(btn) {
  for (let i = 0; i < btn.parentNode.children.length; i++) {
    let e = btn.parentNode.children.item(i);
    e.classList.remove("btn-info");
    e.classList.add("btn-outline-info");
  }

  btn.classList.remove("btn-outline-info");
  btn.classList.add("btn-info");

  document.querySelector("input[type='hidden'][name='amount']").value = btn.getAttribute("value") || btn.value;
}