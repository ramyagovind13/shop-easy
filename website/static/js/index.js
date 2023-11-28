const categoryList = document.getElementById("categoryList");
const productCards = document.querySelectorAll("[data-category]");
const originalCategoryList = categoryList.innerHTML;

categoryList.addEventListener("click", (event) => {
  const selectedCategory = event.target.getAttribute("data-category");

  categoryList.innerHTML = originalCategoryList;

  productCards.forEach((card) => {
    const cardCategory = card.getAttribute("data-category");
    if (selectedCategory === "all" || selectedCategory === cardCategory) {
      card.style.display = "block";
    } else {
      card.style.display = "none";
    }
  });
});
