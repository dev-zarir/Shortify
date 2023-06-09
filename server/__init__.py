from flask import Flask, request
from urllib.parse import urlsplit
from datetime import datetime
from base64 import b64decode
from flask_login import LoginManager, current_user

def init_app(*args, ver:int = 1, **kwargs):
    app = Flask(*args, **kwargs)
    app.config['SECRET_KEY'] = 'KZG8945ViAmkXIfipG12MIGb3oHfvHYLpwJLL2U8'
    app.config['SQLALCHEMY_DATABASE_URI'] = b64decode('cG9zdGdyZXNxbDovL3Nob3J0aWZ5OnYyXzQzNDdtX1RRblBIQ211OVBCZm1KUXBuUFZKalVXQGRiLmJpdC5pbzo1NDMyL3Nob3J0aWZ5L3Nob3J0aWZ5').decode()

    from .models import db, User
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'endpoints.login_endpoint'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user_func(id):
        return User.query.get(int(id))

    from .routes import endpoints
    app.register_blueprint(endpoints)

    @app.context_processor
    def contexts():
        def esc_url(url: str):
            url_path = urlsplit(url).path + '?' + urlsplit(url).query if urlsplit(url).query else urlsplit(url).path
            url = request.url_root[:-1] + url_path if request.url_root.endswith('/') else request.url_root + url_path
            url = url.replace('https:', '').replace('http:', '')
            return url

        return dict(
            esc_url=esc_url,
            current_year=datetime.now().strftime('%Y'),
            app_version=ver,
            user=current_user,
        )

    return app