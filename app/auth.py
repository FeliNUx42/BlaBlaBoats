from crypt import methods
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from .forms.auth import SignupForm, ConfirmForm, ResetRequestForm, ResetPasswordForm,LoginForm, ChangePasswordForm
from .models import User
from .emails import send_confirm_email, send_reset_email
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

    send_confirm_email(user)

    flash("Account created successfully.", "success")
    flash("Please verify your account.", "success")

    return redirect(url_for("auth.unconfirmed"))
    
  return render_template("auth/signup.html", form=form)


@auth.route("/confirm", methods=["GET", "POST"])
@login_required
def unconfirmed():
  form = ConfirmForm()

  if current_user.confirmed:
    flash("This account is already verified.", "danger")
    return redirect(url_for("private.dashboard"))

  if form.validate_on_submit():
    send_confirm_email(current_user)

    flash("A confirmation email has been sent. Please verify your account.", "success")

  return render_template("auth/confirm.html", form=form)


@auth.route("/confirm/<token>")
@login_required
def confirm_account(token):
  if current_user.confirmed:
    flash("This account is already verified.", "danger")
    return redirect(url_for("private.dashboard"))

  user, command = User.verify_token(token)

  if not user or command != "confirm_email" or user != current_user:
    flash("This is an expired or invalid token.", "danger")
    return redirect(url_for("auth.unconfirmed"))
  
  user.confirmed = True
  db.session.commit()

  flash("Your account has been verified successfully.", "success")

  return redirect(url_for("private.dashboard"))


@auth.route("/reset-password", methods=["GET", "POST"])
def reset_request():
  form = ResetRequestForm()

  if current_user.is_authenticated:
    flash("You are already logged in.", "danger")
    return redirect(url_for("private.dashboard"))

  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()

    if user: send_reset_email(user)

    flash("An email has been sent with further instructions...", "success")
    return redirect(url_for("auth.login"))

  return render_template("auth/reset_request.html", form=form)


@auth.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
  form = ResetPasswordForm()

  if current_user.is_authenticated:
    flash("You are already logged in.", "danger")
    return redirect(url_for("private.dashboard"))
  
  user, command = User.verify_token(token)

  if not user or command != "reset_password":
    flash("This is an expired or invalid token.", "danger")
    return redirect(url_for("auth.reset_request"))
  
  if form.validate_on_submit():
    user.password = form.password.data

    db.session.commit()

    flash("Your password has been saved successfully.", "success")
    return redirect(url_for("auth.login"))

  return render_template("auth/reset_password.html", form=form)
  

@auth.route("/login", methods=["GET", "POST"])
def login():
  form = LoginForm()

  if current_user.is_authenticated:
    flash("You are already logged in.", "danger")
    return redirect(url_for("private.dashboard"))

  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()

    login_user(user, remember=form.remember.data)
    flash("Logged in successfully.", "success")

    next_page = request.args.get("next")

    return redirect(next_page or url_for("profile.user_page", uid=user.uid))
    
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
    current_user.password = form.n_password.data
    db.session.commit()

    flash("Password changed successfully.", "success")

    return redirect(url_for("profile.user_page", uid=current_user.uid))
    
  return render_template("auth/security.html", form=form)
