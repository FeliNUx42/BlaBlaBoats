from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from .forms import SignupForm, LoginForm
from .models import User
from . import db
import os


auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
  form = SignupForm()

  if form.validate_on_submit():
    user = User()
    user.uid = os.urandom(8).hex()
    user.username = form.username.data
    user.email = form.email.data
    user.first_name = form.first_name.data
    user.last_name = form.last_name.data
    user.password = form.password.data

    db.session.add(user)
    db.session.commit()

    login_user(user, remember=True)

    flash("Account created successfully.", "success")

    return redirect(url_for("profile.prof", uid=user.uid))

  return render_template("auth/signup.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
  form = LoginForm()

  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user and user.verify_password(form.password.data):
      login_user(user, remember=form.remember.data)

      flash("Logged in successfully.", "success")

      return redirect(url_for("profile.prof", uid=user.uid))
    
    flash("Wrong username or password.", "danger")

  return render_template("auth/login.html", form=form)


@login_required
@auth.route("/logout")
def logout():
  logout_user()

  flash("Logged out successfully.", "success")
  
  return redirect(url_for("home.index"))