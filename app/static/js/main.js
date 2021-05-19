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
const formOnIndex = document.querySelector(".form-index");

preloader
  .querySelector(".spinner-border")
  .classList.add(`text-${bootstrapColors[Math.floor(Math.random() * 8)]}`);

document.addEventListener("DOMContentLoaded", function () {
  setTimeout(function () {
    preloader.style.display = "none";
  }, 600);
});

if (createPostButton) {
  createPostButton.addEventListener("click", function () {
    if (createPostButton.innerHTML === "Create post") {
      formOnIndex.style.maxHeight = formOnIndex.scrollHeight + "px";
      formOnIndex.style.opacity = 1;
      formOnIndex.style.visibility = "visible";
      createPostButton.innerHTML = "Cancel";
    } else {
      formOnIndex.style.maxHeight = 0;
      formOnIndex.style.opacity = 0;
      formOnIndex.style.visibility = "hidden";
      createPostButton.innerHTML = "Create post";
    }
  });
}
