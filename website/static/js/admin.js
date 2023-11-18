document.addEventListener("DOMContentLoaded", function () {
  var adminList = document.getElementById("adminList");
  var contentContainer = document.getElementById("content-container");

  adminList.addEventListener("click", function (event) {
    event.preventDefault();

    var target = event.target.getAttribute("data-target");

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
});
