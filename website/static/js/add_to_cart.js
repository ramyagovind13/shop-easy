document.querySelectorAll(".addToCartButton").forEach(function (button) {
  button.addEventListener("click", function () {
    var sku = this.getAttribute("data-sku");
    var quantity = document.getElementById("quantity_" + sku).value;
    addToCart(sku, quantity);
  });
});

function addToCart(product_id, quantity) {
  console.log("Adding to cart:", product_id, "Quantity:", quantity);
  var data = {
    productId: product_id,
    quantity: quantity,
  };

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "student/add-to-cart", true);
  xhr.setRequestHeader("Content-Type", "application/json");

  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4) {
      if (xhr.status == 200) {
        var successAlert = document.createElement("div");
        successAlert.className = "alert alert-success";
        successAlert.role = "alert";
        successAlert.innerHTML = "Product added to cart successfully !";

        document.getElementById("alert-container").appendChild(successAlert);

        setTimeout(function () {
          successAlert.parentNode.removeChild(successAlert);
        }, 2000);
      } else {
        var errorAlert = document.createElement("div");
        errorAlert.className = "alert alert-danger";
        errorAlert.role = "alert";
        errorAlert.innerHTML = "Failed to add product to cart !";

        document.getElementById("alert-container").appendChild(errorAlert);

        setTimeout(function () {
          errorAlert.parentNode.removeChild(errorAlert);
        }, 2000);
      }
    }
  };
  xhr.send(JSON.stringify(data));
}
