// show tab if has tab in agrs
function switchTab() {
  let args = new URLSearchParams(document.location.search);
  if (!args.has("tab")) return;

  let tab = document.querySelector(`ul.nav-tabs .nav-link[href="#${args.get("tab")}"]`);
  if (!tab) return;

  $(tab).tab("show");
}

switchTab();

// change filename
$(".custom-file-input").on("change", function() {
  var fileName = $(this).val().split("\\").pop();
  $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});

// set max-length for text
$("*[max-length]").each(function() {
  let max = Number($(this).attr("max-length"));
  if ($(this).html().length > max ) {
    $(this).html($(this).html().substr(0, max)+"...")
  }
});

// initialise popovers (https://getbootstrap.com/docs/4.0/components/popovers/)
$('[data-toggle="popover"]').popover({ html: true });

// app/donate.py
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

function test() {
  console.log("hello world");
}