from flask import (
    Blueprint,
    request,
    render_template,
    jsonify,
    redirect,
    abort
)
from .models import (
    db,
    User,
    Short_URL,
    Redirect_Types
)
from urllib.parse import (
    unquote_plus,
    urlparse
)
from string import (
    ascii_letters,
    digits
)
from random import (
    choices
)

endpoints = Blueprint('endpoints', __name__)
disallowed_slugs = ['login', 'register', 'panel', 'lookup']

@endpoints.route('/', methods=["GET", "POST"])
def home_endpoint():
    if request.method == 'POST':
        long_url = unquote_plus(request.form.get('url', ''))
        if not long_url:
            return jsonify(success=False, msg='URL cannot be empty!', type='warning', timeout=10000)
        if not is_valid_url(long_url):
            return jsonify(success=False, msg='Looks like URL is not valid!', type='warning', timeout=10000)
        slug = get_random_slug()
        url_db = Short_URL(slug_text=slug, org_url=long_url)
        db.session.add(url_db)
        db.session.commit()
        return jsonify(success=True, short_url=request.url_root + slug, msg='URL shortened successfully', type='success', timeout=3000)

    return render_template('home.html')

@endpoints.route('/login/', methods=["GET", "POST"])
def login_endpoint():
    return render_template('login.html')

@endpoints.route('/register/', methods=["GET", "POST"])
def register_endpoint():
    return render_template('register.html')

@endpoints.route('/panel/', methods=["GET", "POST"])
def dashboard_endpoint():
    return render_template('dashboard.html')

@endpoints.route('/lookup/', methods=["GET", "POST"])
def lookup_endpoint():
    return render_template('lookup.html')

@endpoints.route('/<slug>/', methods=["GET", "POST"])
def redirect_endpoint(slug):
    url_db = Short_URL.query.filter_by(slug_text=slug).first()
    if not url_db:
        return abort(404)

    title = url_db.title
    description = url_db.description
    org_url = url_db.org_url
    redirect_type = url_db.redirect_type
    url_db.visits += 1
    db.session.commit()

    resp_html = "<head>"
    if title:
        resp_html += f'<title>{title}</title><meta property="og:title" content="{title}" />'
    if description:
        resp_html += f'<meta name="description" content="{description}"><meta property="og:description" content="{description}" />'
    if redirect_type == Redirect_Types.META:
        resp_html += f'<meta http-equiv="refresh" content="0; URL=\'{org_url}\'" />'
    if redirect_type == Redirect_Types.SCRIPT:
        resp_html += f'<script>window.location.href = "{org_url}"</script>'
    resp_html += '</head>'

    if redirect_type == Redirect_Types.HTTP:
        return redirect(org_url)
    else:
        return resp_html


# ========== Functions ========
def is_valid_url(url):
    wide_url = urlparse(url)
    return wide_url.scheme and wide_url.netloc

def get_random_slug(l:int=4):
    while 1:
        slug = ''.join(choices(ascii_letters + digits, k=l))
        if not Short_URL.query.filter_by(slug_text=slug).first():
            return slug


        
