from flask import Blueprint, redirect, render_template, jsonify, url_for
from .models import Trip, User
from .forms import SearchForm
from . import db

home = Blueprint("home", __name__)

@home.route("/")
def index():
  return render_template("main/home.html")

@home.route("/search")
def search():
  form = SearchForm()

  if form.validate():
    trips = Trip.search(form.q.data)
    users = User.search(form.q.data)
    return render_template("main/search.html", query=form.q.data, trips=trips, users=users)

  return redirect(url_for("home.index"))