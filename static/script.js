var prevScrollPos = window.pageYOffset;
window.addEventListener('scroll', function() {
  let currentScrollPos = window.pageYOffset;
  if (prevScrollPos >= currentScrollPos) {
    document.querySelector(".sticky-header").classList.remove("hidden");
    document.querySelector('html').classList.add('show-header');
  } else {
    document.querySelector(".sticky-header").classList.add("hidden");
    document.querySelector('html').classList.remove('show-header');
  }
  prevScrollPos = currentScrollPos;
});

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
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
  await sleep(3000);
  while (true) {
    for(let tag of all_tags){
      for(let char of $('#animated-tags').text()){
        $('#animated-tags').text($('#animated-tags').text().slice(0, -1));
        await sleep(30);
      };
      for(let char of tag){
        $('#animated-tags').text($('#animated-tags').text() + char);
        await sleep(30);
      };
      await sleep(3000);
    };
  };
};

// Alert Msg
function show_msg(msg, type = 'primary', time = 3000){
  let id = Math.random()*10**17;
  let icon_ver = 'bi';
  let close_btn_click = "close_msg(this.parentElement.getAttribute('id'))"
  let elem = document.createElement("div");
  elem.setAttribute("id",id);
  elem.setAttribute("class", `alert alert-${type}`)
  elem.setAttribute("style", `--time: ${time}ms; --time-color: var(--bs-${type});`)
  let html = `<span class="loader"></span>`;
  if (type == 'primary'){
    html += `<i class="${icon_ver} bi-info-circle"></i>`;
  } else if (type == 'warning') {
    html += `<i class="${icon_ver} bi-exclamation-triangle"></i>`;
  } else if (type == 'danger') {
    html += `<i class="${icon_ver} bi-x-circle"></i>`;
  } else if (type == 'success') {
    html += `<i class="${icon_ver} bi-check-circle"></i>`;
  }
  html += `<div class="content me-2">${msg}</div>`;
  html += `<button class="btn-close shadow-none my-auto" style="transition: all 0.3s ease;" onclick="${close_btn_click}"></button>`;
  elem.innerHTML=html
  document.getElementById('alert').prepend(elem);
  setTimeout(() => {document.getElementById(id).classList.add('active')}, 10);
  document.getElementById(id).querySelector('span.loader').addEventListener('animationend', function () {close_msg(id)});
}
function close_msg (id) {
  document.getElementById(id).classList.remove('active');
  document.getElementById(id).addEventListener("transitionend", function () {
    try {
    document.getElementById(id).remove();
    } catch(e) {
      window.err_msg += '\n\n' + e;
    }
  })
}

function copyLink(elem) {
  let btn = $(elem);
  let copyText = btn.parent().find('input').val();
  navigator.clipboard.writeText(copyText)
      .then(function() {
        btn.removeClass('bi-clipboard2').addClass('bi-clipboard2-check success');
        setTimeout(function() {
          btn.addClass('bi-clipboard2').removeClass('bi-clipboard2-check success');
        }, 3000);
      })
      .catch(function(err) {
        show_msg('Sorry, clipboard is not supported.', 'danger', 10000);
      });
}

window.addEventListener('load', function () {
  window.dispatchEvent(new Event('scroll'));
})

// DEVELOPMENT CODE
function reloadWebPage() {
  fetch(window.location.href).then(resp => resp.text()).then( html => document.open() && document.write(html) && document.close());
}
document.addEventListener('keydown', function(event) {
  if (event.ctrlKey && event.keyCode === 82) {
    event.preventDefault();reloadWebPage();
  }
});