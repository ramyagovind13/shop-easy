var contentContainer = document.getElementById("content-container");
document.addEventListener("DOMContentLoaded", function () {
  var adminList = document.getElementById("adminList");

  adminList.addEventListener("click", function (event) {
    event.preventDefault();

    var target = event.target.getAttribute("data-target");
    console.log(target);

    if (target === "dashboard") {
      load_dashboard_content();
    } else {
      load_content(target);
    }
  });

  function load_dashboard_content() {
    var imageUrl = "/static/img/admin.webp";

    contentContainer.innerHTML =
      '<div class="p-4"><img src="' +
      imageUrl +
      '" alt="Dashboard Image" class="img-fluid"></div>';
  }

  load_dashboard_content();
});

function load_content(target) {
  $.ajax({
    url: "/" + target,
    type: "GET",
    success: function (data) {
      contentContainer.innerHTML = '<div class="p-4">' + data + "</div>";
    },
    error: function () {
      contentContainer.innerHTML =
        '<div class="p-4">Error loading content</div>';
    },
  });
}

var contentContainer = document.getElementById("content-container");

$(document).on("click", ".edit-product", function (event) {
  event.preventDefault();
  var sku = $(this).data("sku");
  load_update_product_form(sku);
});

function load_update_product_form(sku) {
  $.ajax({
    url: "/edit_product/" + sku,
    type: "GET",
    success: function (data) {
      contentContainer.innerHTML = '<div class="p-4">' + data + "</div>";
    },
    error: function () {
      contentContainer.innerHTML =
        '<div class="p-4">Error loading update product form</div>';
    },
  });
}

$(document).on("click", ".delete-product", function (event) {
  event.preventDefault();
  var sku = $(this).data("sku");
  load_delete_product_form(sku);
});

function load_delete_product_form(sku) {
  $.ajax({
    url: "/delete_product/" + sku,
    type: "DELETE",
    success: function (data) {
      load_content("products");
    },
    error: function () {
      load_content("products");
    },
  });
}
