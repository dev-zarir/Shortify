from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy(engine_options={"pool_recycle": 55})

class Redirect_Types(Enum):
    HTTP = 'HTTP'
    META = 'META'
    SCRIPT = 'SCRIPT'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    urls = db.relationship('Short_URL', backref='user', lazy=True)

class Short_URL(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    slug_text = db.Column(db.String(255), unique=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(2048))
    org_url = db.Column(db.String(2048), nullable=False)
    visits = db.Column(db.Integer, default=0, nullable=False)
    redirect_type = db.Column(db.Enum(Redirect_Types), nullable=False, default=Redirect_Types.HTTP)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), default=None)

