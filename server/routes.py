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
from flask_login import(
    login_user,
    login_required,
    logout_user,
    current_user
)
from urllib.parse import (
    unquote_plus,
    urlparse
)
from string import (
    ascii_letters,
    digits
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from random import (
    choices
)
from requests import (
    get
)
import re

endpoints = Blueprint('endpoints', __name__)
LOCKED_SLUG = ['login', 'register', 'panel', 'logout']
CUTTLY_API_KEY = "9f77d8e31d30723671318aec49dd56174be5a"

@endpoints.route('/favicon.ico/', methods=["GET", "POST"])
def favicon_endpoint():
    return redirect('/static/favicon.ico')

@endpoints.route('/', methods=["GET", "POST"])
def home_endpoint():
    if current_user.is_authenticated:
        return redirect('/panel/')
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


@endpoints.route('/logout/', methods=["GET", "POST"])
@login_required
def logout_endpoint():
    logout_user()
    return redirect('/')


@endpoints.route('/login/', methods=["GET", "POST"])
def login_endpoint():
    if current_user.is_authenticated:
        return redirect('/panel/')
    if request.method == 'POST':
        email = unquote_plus(request.form.get('email', ''))
        password = unquote_plus(request.form.get('pass', ''))
        if not (email and password):
            return jsonify(success=False, msg='Please fill up all fields!', type='warning', timeout=10000)
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify(success=False, msg='User not found! Email does not exists.', type='warning', timeout=10000)
        if not check_password_hash(user.password, password):
            return jsonify(success=False, msg='The provided password is not valid.', type='warning', timeout=10000)

        login_user(user, remember=True)
        return jsonify(success=True, msg='You\'re successfully logged in.', type='success', timeout=3000)

    return render_template('login.html')


@endpoints.route('/register/', methods=["GET", "POST"])
def register_endpoint():
    if current_user.is_authenticated:
        return redirect('/panel/')
    if request.method == 'POST':
        email = unquote_plus(request.form.get('email', ''))
        password = unquote_plus(request.form.get('pass', ''))
        cpassword = unquote_plus(request.form.get('cpass', ''))
        if not (email and password and cpassword):
            return jsonify(success=False, msg='Please fill up all fields!', type='warning', timeout=10000)
        if User.query.filter_by(email=email).first():
            return jsonify(success=False, msg='Email address already exists!', type='warning', timeout=10000)
        if not is_valid_email(email):
            return jsonify(success=False, msg='Please provide a valid email!', type='warning', timeout=10000)
        if len(password) < 6:
            return jsonify(success=False, msg='Please provide a password of at least 6 characters!', type='warning', timeout=10000)
        if password != cpassword:
            return jsonify(success=False, msg='Please make sure both of the passwords are same!', type='warning', timeout=10000)

        new_user = User(email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        return jsonify(success=True, msg='Account registered successfully! Please login.', type='success', timeout=3000)

    return render_template('register.html')


@endpoints.route('/panel/', methods=["GET", "POST"])
@login_required
def dashboard_endpoint():
    if request.method == 'POST':
        redirect_type = unquote_plus(request.form.get('redirect-type', ''))
        redirect_type = Redirect_Types.SCRIPT if redirect_type == 'script' else Redirect_Types.META if redirect_type == 'meta' else Redirect_Types.HTTP
        alias = unquote_plus(request.form.get('alias', ''))
        if alias:
            if not is_valid_slug(alias):
                return jsonify(success=False, msg='Invalid Alias! Please remove speacial characters.', type='warning', timeout=10000)
            if Short_URL.query.filter_by(slug_text=alias).first():
                return jsonify(success=False, msg='Alias already exists!', type='warning', timeout=10000)
        else:
            alias = get_random_slug()
        long_url = unquote_plus(request.form.get('url', ''))
        title = unquote_plus(request.form.get('title', ''))
        description = unquote_plus(request.form.get('description', ''))
        user_id = current_user.id

        url_db = Short_URL(slug_text=alias, title=title, description=description, org_url=long_url, redirect_type=redirect_type, user_id=user_id)
        db.session.add(url_db)
        db.session.commit()

        return jsonify(success=True, msg='URL shortened successfully.', type='success', timeout=3000, id=url_db.id, short_url=request.url_root + alias, alias=alias, title=title, description=description, org_url=long_url, redirect_type=redirect_type.value)
    
    page_no = request.args.get('page', 1, type=int)
    page_size = 10

    user_links = Short_URL.query.filter_by(user_id=current_user.id).order_by(Short_URL.id.desc())
    total_url = user_links.count()
    total_page = (total_url - 1) // page_size + 1
    # if total_url < page_size * (page_no - 1):
    if page_no > total_page or page_no < 1:
        page_no = 1
    user_links = user_links.paginate(page=page_no, per_page=page_size, error_out=False)

    pages_list = [page_no - 1, page_no, page_no + 1]
    if 0 in pages_list:
        pages_list.remove(0)
    if page_no + 1 > total_page:
        pages_list.remove(page_no + 1)
    if 1 not in pages_list:
        if 2 in pages_list:
            pages_list = [1] + pages_list
        else:
            pages_list = [1, None] + pages_list
    if total_page not in pages_list:
        if total_page - 1 in pages_list:
            pages_list += [total_page]
        else:
            pages_list += [None, total_page]

    return render_template('dashboard.html', links=user_links, total_url=total_url, page_no=page_no, total_page=total_page, page_size=page_size, pages_list=pages_list)

@endpoints.route('/panel/edit/', methods=["POST"])
@login_required
def url_edit_endpoint():
    url_id = request.form.get('id', '')
    url_db = Short_URL.query.get(int(url_id))
    if not url_db:
        return jsonify(success=False, msg='URL is not found.', type='warning', timeout=10000)
    if url_db.user_id != current_user.id:
        return jsonify(success=False, msg='You do not own this url.', type='warning', timeout=10000)
    redirect_type = unquote_plus(request.form.get('redirect-type', ''))
    redirect_type = Redirect_Types.SCRIPT if redirect_type == 'script' else Redirect_Types.META if redirect_type == 'meta' else Redirect_Types.HTTP
    alias = unquote_plus(request.form.get('alias', ''))
    if alias:
        if not is_valid_slug(alias):
            return jsonify(success=False, msg='Invalid Alias! Please remove speacial characters.', type='warning', timeout=10000)
        if alias != url_db.slug_text:
            if Short_URL.query.filter_by(slug_text=alias).first():
                return jsonify(success=False, msg='Alias already exists!', type='warning', timeout=10000)
    else:
        alias = get_random_slug()
    long_url = unquote_plus(request.form.get('url', ''))
    title = unquote_plus(request.form.get('title', ''))
    description = unquote_plus(request.form.get('description', ''))

    url_db.redirect_type = redirect_type
    url_db.slug_text = alias
    url_db.org_url = long_url
    url_db.title = title
    url_db.description = description

    db.session.commit()
    return jsonify(success=True, msg='URL updated successfully.', type='success', timeout=3000, short_url=request.url_root + alias, alias=alias, title=title, description=description, org_url=long_url, redirect_type=redirect_type.value)


@endpoints.route('/panel/delete/', methods=["POST"])
@login_required
def url_delete_endpoint():
    url_id = request.form.get('id', -1, type=int)
    if url_id == -1:
        return jsonify(success=False, msg='Please send a valid url id.', type='warning', timeout=10000)
    url_db = Short_URL.query.get(int(url_id))
    if not url_db:
        return jsonify(success=False, msg='URL is not found.', type='warning', timeout=10000)
    if url_db.user_id != current_user.id:
        return jsonify(success=False, msg='You don\'t own this url.', type='warning', timeout=10000)

    db.session.delete(url_db)
    db.session.commit()

    return jsonify(success=True, msg='URL deleted successfully.', type='success', timeout=3000)


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

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    is_ok = re.match(pattern, email) is not None
    if not is_ok: return False
    try:
        resp = get('https://nobounce.onrender.com/isdelivrable/' + email)
        return True if resp.json().get('Delivrable') == 'True' else False
    except:
        return True

def is_valid_slug(slug):
    if slug.lower() in LOCKED_SLUG:
        return False
    pattern = r'^[a-z0-9]+(?:[_-][a-z0-9]+)*$'
    return bool(re.match(pattern, slug))

def cuttly_shorturl(long_url, alias=None):
    params = {
        'key': CUTTLY_API_KEY,
        'short': long_url,
        'noTitle': 1
    }
    if alias:
        if not is_valid_slug(alias):
            raise Exception('Invalid Alias. Special characters isn\'t supported')
        params['name'] = alias
    resp = get('http://cutt.ly/api/api.php', params=params)
    errors = {
        1: 'The link has already been shortened',
        2: 'The entered link is not a link',
        3: 'The preferred link alias is already taken',
        5: 'The link has not passed the validation. Includes invalid characters',
        6: 'The link provided is from a blocked domain',
        8: 'Cutt.ly monthly limit reached'
    }
    try:
        url_info = resp.json().get('url')
        scode = url_info.get('status')
    except:
        raise Exception("Unknown Error: " + resp.text)
    if scode != 7:
        if scode in list(errors):
            raise Exception(errors.get(scode))
        else:
            raise Exception("Unknown Error: " + resp.text)
    return url_info.get('shortLink')


def cuttly_editurl(short_link, new_alias):
    params = {
        'key': CUTTLY_API_KEY,
        'edit': short_link,
        'name': new_alias
    }
    if not is_valid_slug(new_alias):
        raise Exception('Invalid Alias. Special characters isn\'t supported')
    key = "9f77d8e31d30723671318aec49dd56174be5a"
    resp = get('http://cutt.ly/api/api.php', params=params)
    errors = {
        2: 'Alias is already taken.',
        3: 'The url doesn\'t exists in your account',
    }
    try:
        scode = resp.json().get('status')
    except:
        raise Exception('Error: ' + resp.text)
    if scode != 1:
        if scode in list(errors):
            raise Exception(errors.get(scode))
        else:
            raise Exception('Unknown Error')
    return True

