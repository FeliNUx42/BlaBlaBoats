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