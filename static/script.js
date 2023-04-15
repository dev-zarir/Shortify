var prevScrollPos = window.pageYOffset;
window.onscroll = function() {
  let currentScrollPos = window.pageYOffset;
  if (prevScrollPos > currentScrollPos) {
    document.querySelector(".sticky-header").classList.remove("hidden");
  } else {
    document.querySelector(".sticky-header").classList.add("hidden");
  }
  prevScrollPos = currentScrollPos;
};
