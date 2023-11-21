function validateForm() {
  var name = document.getElementById("name");
  var category = document.getElementById("category");
  var description = document.getElementById("description");
  var quantity = document.getElementById("quantity");

  if (name.value === "") {
    alert("Please enter a product name.");
    return false;
  }

  if (category.value === "") {
    alert("Please select a category.");
    return false;
  }

  if (description.value === "") {
    alert("Please enter a description.");
    return false;
  }

  if (quantity.value === "") {
    alert("Please enter quantity.");
    return false;
  }

  return true;
}

document.querySelector("form").addEventListener("submit", function (event) {
  if (!validateForm()) {
    event.preventDefault();
  }
});
