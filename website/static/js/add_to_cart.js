document.querySelectorAll(".addToCartButton").forEach(function (button) {
  button.addEventListener("click", function () {
    var sku = this.getAttribute("data-sku");
    var quantity = document.getElementById("quantity_" + sku).value;
    addToCart(sku, quantity);
  });
});

function addToCart(productId, quantity) {
  console.log("Adding to cart:", productId, "Quantity:", quantity);
  var data = {
    productId: productId,
    quantity: quantity,
  };

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/add-to-cart", true);
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
