from flask import Blueprint, render_template
from app.controllers.auth_controller import login

main = Blueprint('main', __name__)

# HOME PAGE
@main.route('/')
def home():
    return render_template("index.html")

# LOGIN PAGE
@main.route('/login', methods=['GET', 'POST'])
def login_route():
    return login()