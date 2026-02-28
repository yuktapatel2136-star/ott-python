from flask import render_template, redirect, url_for, flash
from app.forms.auth_from import LoginForm
from app.models.user_model import User
from app import db

def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            flash("Login Successful!")
            return redirect(url_for('main.login_route'))

        else:
            flash("Invalid Email or Password")

    return render_template("login.html", form=form)