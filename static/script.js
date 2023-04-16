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

function sleep(s) {
  return new Promise(resolve => setTimeout(resolve, s*1000));
}

async function run_animated_tags() {
  let all_tags = [
    "Transforming long links into short and sweet URLs",
    "Get more out of your links with our URL shortener",
    "Say more with less - shorten your URLs today",
    "Effortlessly share your links with our URL shortener",
    "Simplify your links with our URL shortening service",
    "Shorten URLs, share more, worry less",
    "Make your links stand out with our URL shortener",
    "Short and sweet - the power of our URL shortener",
    "Shorten, share, succeed with our URL shortening tool",
    "Elevate your link game with our URL shortener",
    "Get your message across faster with our URL shortening service",
    "Less is more - shorten your links with us",
    "Shorten your URLs, lengthen your reach",
  ];
  await sleep(5);
  while (true) {
    for(let tag of all_tags){
      for(let char of $('#animated-tags').text()){
        $('#animated-tags').text($('#animated-tags').text().slice(0, -1));
        await sleep(0.03);
      };
      for(let char of tag){
        $('#animated-tags').text($('#animated-tags').text() + char);
        await sleep(0.03);
      };
      await sleep(3);
    };
  };
};


// DEVELOPMENT CODE
function reloadWebPage() {
  fetch(window.location.href).then(resp => resp.text()).then( html => document.open() && document.write(html) && document.close());
}
document.addEventListener('keydown', function(event) {
  if (event.ctrlKey && event.keyCode === 82) {
    event.preventDefault();reloadWebPage();
  }
});