from flask import Blueprint, request, render_template
from .models import User, Short_URL, Redirect_Types

endpoints = Blueprint('endpoints', __name__)

@endpoints.route('/', methods=["GET", "POST"])
def home_endpoint():
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


