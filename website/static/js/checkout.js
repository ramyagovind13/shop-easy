$(document).ready(function () {
  $("#checkoutBtn").on("click", function () {
    var cartDetailsJson = $(this).attr("data-cart-details");
    cartDetailsJson = cartDetailsJson.replace(/'/g, '"');
    var cartDetails = JSON.parse(cartDetailsJson);

    $.ajax({
      type: "POST",
      url: "student/place-order",
      contentType: "application/json",
      data: JSON.stringify({ cartDetails: cartDetails }),
      success: function (response) {
        console.log(response);
        window.location.href = "/get-inventory";
      },
      error: function (error) {
        console.error("Error:", error);
      },
    });
  });
});
