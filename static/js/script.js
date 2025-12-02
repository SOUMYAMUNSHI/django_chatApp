let user_name = document.getElementsByClassName("user-name");
console.log(user_name);

let img = document.getElementById("img");
img.addEventListener("mouseenter", () => {
  let mouse_hover = document.getElementById("mouse-hover");
  let img = document.getElementById("user-image");
  mouse_hover.style.display = "flex";
  img.style.filter = "blur(1px)";
});

img.addEventListener("mouseout", () => {
  let mouse_hover = document.getElementById("mouse-hover");
  mouse_hover.style.display = "none";
  let img = document.getElementById("user-image");
  img.style.filter = "blur(0px)";
});
