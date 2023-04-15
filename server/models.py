from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(engine_options={"pool_recycle": 55})

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


