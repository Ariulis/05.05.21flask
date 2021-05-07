const preloader = document.querySelector(".page-preloader");
const bootstrapColors = [
  "primary",
  "danger",
  "success",
  "warning",
  "info",
  "secondary",
  "light",
  "dark",
];
const createPostButton = document.querySelector(".create-post");

preloader
  .querySelector(".spinner-border")
  .classList.add(`text-${bootstrapColors[Math.floor(Math.random() * 8)]}`);

document.addEventListener("DOMContentLoaded", function () {
  setTimeout(function () {
    preloader.style.display = "none";
  }, 600);

  if (createPostButton) {
    createPostButton.previousElementSibling.style.display = "none";
  }
});

createPostButton.addEventListener("click", function () {
  if (createPostButton.innerHTML === "Create post") {
    createPostButton.previousElementSibling.style.display = "block";
    createPostButton.innerHTML = "Cancel";
  } else {
    createPostButton.previousElementSibling.style.display = "none";
    createPostButton.innerHTML = "Create post";
  }
});
