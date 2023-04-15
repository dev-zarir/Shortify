from flask import Blueprint, request, render_template
from .models import User

endpoints = Blueprint('endpoints', __name__)

@endpoints.route('/')
def home_endpoint():
    return render_template('home.html')

@endpoints.route('/login/')
def login_endpoint():
    return render_template('login.html')

@endpoints.route('/register/')
def register_endpoint():
    return render_template('register.html')

@endpoints.route('/panel/')
def dashboard_endpoint():
    return render_template('dashboard.html')

@endpoints.route('/lookup/')
def lookup_endpoint():
    return render_template('lookup.html')


