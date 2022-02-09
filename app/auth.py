from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from .forms import SignupForm, LoginForm, ChangePasswordForm
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

    return redirect(url_for("profile.user_page", uid=user.uid))

  return render_template("auth/signup.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
  form = LoginForm()

  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user and user.verify_password(form.password.data):
      login_user(user, remember=form.remember.data)

      flash("Logged in successfully.", "success")

      return redirect(url_for("profile.user_page", uid=user.uid))
    
    flash("Wrong username or password.", "danger")

  return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
  logout_user()

  flash("Logged out successfully.", "success")
  
  return redirect(url_for("home.index"))


@auth.route("/security", methods=["GET", "POST"])
@login_required
def security():
  form = ChangePasswordForm()

  if form.validate_on_submit():
    if current_user.verify_password(form.o_password.data):
      current_user.password = form.n_password.data

      db.session.commit()

      flash("Password changed successfully.", "success")
      return redirect(url_for("profile.user_page", uid=current_user.uid))
      
    flash("The old password doesn't match.", "danger")

  return render_template("auth/security.html", form=form)
