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
  if (btn.hasClass('success')){return}
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

function togglePasswordShow(elem) {
  let btn = $(elem);
  let input = btn.parent().find('input');
  if(input.attr('type') == 'password'){
    input.attr('type', 'text');
    btn.removeClass('bi-eye').addClass('bi-eye-slash');
  } else {
    input.attr('type', 'password');
    btn.addClass('bi-eye').removeClass('bi-eye-slash');
  }
}


// Home Page Script
$('#shorting-form').submit(function (event) {
  event.preventDefault();
  let form = $(this);
  let formData = form.serialize()
  form.find('*').prop('disabled', true);
  $.ajax({
    url: window.location.href,
    type: 'POST',
    data: formData,
    success: function (r, s) {
      if(r.success) {
        if(window.location.protocol == 'https:'){
          r.short_url = r.short_url.replace('http://', 'https://')
        }
        link_div = $(`
        <div class="input-icon-group fade">
            <input class="form-control" type="text" value="${r.short_url}" readonly disabled>
            <i class="bi bi-clipboard2" onclick="copyLink(this)"></i>
        </div>
        `);
        $('#url-list').prepend(link_div);
        setTimeout(() => {
          link_div.addClass('show glow')
        }, 50);
        form.find('#url').val('');
      }
      show_msg(r.msg, r.type, r.timeout)
      form.find('*').prop('disabled', false);
    },
    error: function (r, s) {
      show_msg('Sorry, something went wrong.', 'danger', 10000)
      form.find('*').prop('disabled', false);
    }
  })
})

// Login Page Script
$('#login-form').submit(function (event) {
  event.preventDefault();
  let form = $(this);
  let email = form.find('#email').val();
  let pass = form.find('#pass').val();
  let formData = form.serialize();
  form.find('*').prop('disabled', true);
  $.ajax({
      url: window.location.href,
      type: 'POST',
      data: formData,
      success: function (r, s) {
          if (r.success) {
              setTimeout(() => {
                  window.location.href = '/panel/';
              }, 3000);
          }
          show_msg(r.msg, r.type, r.timeout);
          form.find('*').prop('disabled', false);
      },
      error: function (r, s) {
          show_msg('Sorry, something went wrong.', 'danger', 10000)
          form.find('*').prop('disabled', false);
      }
  })
})

// Register Page Script
$('#register-form').submit(function (event) {
  event.preventDefault();
  let form = $(this);
  let email = form.find('#email').val();
  let pass = form.find('#pass').val();
  let cpass = form.find('#cpass').val();
  let formData = form.serialize();
  if (pass.length < 6) {show_msg('Please provide a password of at least 6 characters!', 'warning', 10000);return false}
  if (pass != cpass){show_msg('Please make sure both of the passwords are same!', 'warning', 10000);return false}
  form.find('*').prop('disabled', true);
  $.ajax({
      url: window.location.href,
      type: 'POST',
      data: formData,
      success: function (r, s) {
          if (r.success) {
              setTimeout(() => {
                  window.location.href = '/login/';
              }, 3000);
          }
          show_msg(r.msg, r.type, r.timeout);
          form.find('*').prop('disabled', false);
      },
      error: function (r, s) {
          show_msg('Sorry, something went wrong.', 'danger', 10000)
          form.find('*').prop('disabled', false);
      }
  })
})

// Dashboard Page Script
$('[id="redirect-type"]').change(function () {
  let select = $(this);
  if (select.val() == 'meta' || select.val() == 'script' ){
    select.parent().parent().find('.more-url-info').show();
  } else{
    select.parent().parent().find('.more-url-info').hide();
  }
})
$('#dash-url-submit').submit(function (event) {
  event.preventDefault();
  let form = $(this);
  let formData = form.serialize();
  form.find('*').prop('disabled', true);
  $.ajax({
    url: '/panel/',
    type: 'POST',
    data: formData,
    success: function (r, s) {
      if (r.success) {
        let title_html = '';
        let description_html = '';
        if(r.redirect_type != 'HTTP') {
          if (r.title) {
            title_html = `<span class="meta-title-sec"><b>Title:</b> <span class="meta-title">${r.title}</span></span>`;
          }
          if (r.description) {
            description_html = `<span class="meta-description-sec"><b>Description:</b> <span class="meta-description">${r.description}</span></span>`;
          }
        }
        let url_item = $(`
        <div class="url-item bg-body-tertiary rounded fade" data-id="${r.id}" data-alias="${r.alias}">
        <div class="url-info">
                  <span class="short_url d-flex gap-2"><b class="text-nowrap">Short URL:</b> <a class="text-decoration-none link-primary" href="${r.short_url}" target="_blank">${r.short_url}</a> <i onclick="DashCopyLink(this, '.short_url a')" class="bi bi-clipboard2"></i><span class="line-spacer"></span></span>
                  <span class="long_url d-flex gap-2"><b class="text-nowrap">Long URL:</b> <a class="text-decoration-none link-primary" href="${r.org_url}" target="_blank">${r.org_url}</a> <i onclick="DashCopyLink(this, '.long_url a')" class="bi bi-clipboard2"></i><span class="line-spacer"></span></span>
                  <span class="redirect_type badge bg-primary">${r.redirect_type}</span>
                  <span class="visits"><span class="badge bg-primary">0</span> visits</span>
                  ${title_html}
                  ${description_html}
              </div>
              <div class="url-action select-none">
                  <i onclick="DashCopyLink(this, '.short_url a')" class="bi bi-clipboard2"></i>
                  <i onclick="window.open($(this).parent().parent().find('.long_url a').attr('href'))" class="bi bi-box-arrow-up-right"></i>
                  <i onclick="openEditModal(this)" class="bi bi-pencil-square"></i>
                  <i onclick="$('#delete_modal').attr('data-id', '{{ item.id }}');delete_modal.show();" class="bi bi-trash"></i>
              </div>
          </div>
        `)
        $('#list-url').prepend(url_item);
        setTimeout(() => {
          url_item.addClass('show glow');
          url_item.on('animationend', function () {
            url_item.addClass('shadow');
          })
        }, 50);
        form.find('input').val('');
      }
      form.find('*').prop('disabled', false);
      show_msg(r.msg, r.type, r.timeout);
    },
    error: function (r, s) {
      form.find('*').prop('disabled', false);
      show_msg('Sorry, something went wrong!', 'danger', 10000);
    }
  })
})

function DashCopyLink(elem, selector) {
  let btn = $(elem);
  let link = btn.parent().parent().find(selector).attr('href');
  navigator.clipboard.writeText(link)
    .then(function () {
      btn.removeClass('bi-clipboard2').addClass('bi-clipboard2-check success');
      setTimeout(function() {
        btn.addClass('bi-clipboard2').removeClass('bi-clipboard2-check success');
      }, 3000);      
    })
    .catch(function (err) {
      show_msg('Sorry, clipboard is not supported.', 'danger', 10000);
    })
}

function deleteURL(elem) {
  let btn = $(elem);
  let url_id = $('#delete_modal').attr('data-id');
  btn.attr('disabled', true);
  $.ajax({
    url: '/panel/delete/',
    type: 'POST',
    data: 'id=' + url_id,
    success: function (r, s) {
      if (r.success){
        $('#delete_modal').removeAttr('data-id');
        $(`.url-item[data-id="${url_id}"]`).remove();
        delete_modal.hide();
      }
      btn.attr('disabled', false);
      show_msg(r.msg, r.type, r.timeout);
    },
    error: function (r, s) {
      btn.attr('disabled', false);
      show_msg('Sorry, something went wrong!', 'danger', 10000);
    }
  })
}

function openEditModal(elem) {
  elem = $(elem);
  let url_item = elem.parent().parent();
  let url_id = url_item.attr('data-id');
  let slug = url_item.attr('data-alias');
  let long_url = url_item.find('.long_url a').attr('href');
  let redirect_type = url_item.find('.redirect_type').text().toLowerCase();
  let title = url_item.find('.meta-title').text();
  let description = url_item.find('.meta-description').text();
  $('#dash-url-edit #url_id_edit').val(url_id);
  $('#dash-url-edit #redirect-type').val(redirect_type);
  $('#dash-url-edit #redirect-type').trigger('change');
  $('#dash-url-edit #title').val(title);
  $('#dash-url-edit #description').val(description);
  $('#dash-url-edit #alias').val(slug);
  $('#dash-url-edit #url').val(long_url);
  edit_modal.show();
}

function saveURLedit(elem) {
  elem = $(elem);
  let form = $('#dash-url-edit');
  let url_id = form.find('#url_id_edit').val();
  let formData = form.serialize();
  elem.attr('disabled', true);
  $.ajax({
    url: '/panel/edit/',
    type: 'POST',
    data: formData,
    success: function (r, s) {
      if (r.success) {
        let url_item = $('.url-item[data-id="' + url_id + '"]');
        url_item.attr('data-alias', r.alias);
        url_item.find('.short_url a').text(r.short_url);
        url_item.find('.short_url a').attr('href', r.short_url);
        url_item.find('.long_url a').text(r.org_url);
        url_item.find('.long_url a').attr('href', r.org_url);
        url_item.find('.redirect_type').text(r.redirect_type);
        url_item.find('.meta-title').text(r.title);
        url_item.find('.meta-description').text(r.description);
        edit_modal.hide();
      }
      elem.attr('disabled', false);
      show_msg(r.msg, r.type, r.timeout);
    },
    error: function (r, s) {
      elem.attr('disabled', false);
      show_msg('Sorry, something went wrong!', 'danger', 10000);
    }
  })
}

window.addEventListener('load', function () {
  window.dispatchEvent(new Event('scroll'));
})
