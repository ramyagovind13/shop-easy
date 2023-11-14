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
    if (xhr.readyState == 4 && xhr.status == 200) {
      console.log("Success:", xhr.responseText);
    } else if (xhr.readyState == 4 && xhr.status != 200) {
      console.error("Error:", xhr.status);
    }
  };

  xhr.send(JSON.stringify(data));
}
