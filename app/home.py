from flask import Blueprint, current_app, render_template, flash, request
from flask_login import current_user
from .models import Trip, User, UserMsg
from .forms.search import SearchForm, ContactForm
import os
from . import db, sitemap


home = Blueprint("home", __name__)

@home.route("/", methods=["GET", "POST"])
def index():
  form = SearchForm()
  c_form = ContactForm()

  if c_form.validate_on_submit():
    msg = UserMsg()
    msg.uid = os.urandom(8).hex()
    msg.email = c_form.email.data
    msg.message = c_form.message.data

    if current_user.is_authenticated:
      msg.user = current_user
    
    db.session.add(msg)
    db.session.commit()

    flash("Message sent successfully.", "success")

  return render_template("main/home.html", form=form, c_form=c_form)


@home.route("/search")
def search():
  form = SearchForm()

  page = request.args.get("page", 1, type=int)

  if form.validate():
    t_query = {"bool": {"must": {}, "filter": []}}

    has_query = bool(form.q.data)
    has_location = bool(form.lat.data is not None and form.lng.data is not None and form.dist.data)
    location_sort = bool(form.lat.data is not None and form.lng.data is not None)
    has_dates = bool(form.start_date.data and form.end_date.data)
    has_type = bool(form.boat_type.data.replace("All", ""))
    has_mode = bool(form.sailing_mode.data.replace("All", ""))
    has_people = bool(form.people.data)

    if has_query:
      t_query["bool"]["must"]["multi_match"] = {
        "query": form.q.data,
        "fields": Trip.__searchable__,
        "fuzziness":"AUTO:3,6"
      }

      u_query = {"multi_match":{"query":form.q.data, "fields":["*"], "fuzziness":"AUTO:3,6"}}
    else:
      t_query["bool"]["must"]["match_all"] = {}

      u_query = {"match_all": {}}
    
    if has_location or has_dates:
      t_query["bool"]["filter"].append({"nested": {"path": "destinations", "inner_hits": {}, "query": {"bool": {"must": []}}}})

      if has_location:
        t_query["bool"]["filter"][0]["nested"]["query"]["bool"]["must"].append({
          "geo_distance" : {
            "distance" : f"{form.dist.data}{form.unit.data}",
              "destinations.location" : {
              "lat" : form.lat.data,
              "lon" : form.lng.data
            }
          }
        })

      if has_dates:
        t_query["bool"]["filter"][0]["nested"]["query"]["bool"]["must"].append({"bool": {"should": [
          {
            "range": {
              "destinations.arrival": {
                "format": "date_optional_time",
                "gte": form.start_date.data.isoformat(),
                "lte": form.end_date.data.isoformat()
              }
            }
          },
          {
            "range": {
              "destinations.departure": {
                "format": "date_optional_time",
                "gte": form.start_date.data.isoformat(),
                "lte": form.end_date.data.isoformat()
              }
            }
          }
        ]}})

    if has_type:
      t_query["bool"]["filter"].append({
        "term": {
          "boat_type": form.boat_type.data
        }
      })

    if has_mode:
      t_query["bool"]["filter"].append({
        "term": {
          "sailing_mode": form.sailing_mode.data
        }
      })

    if has_people:
      t_query["bool"]["filter"].append({
        "range": {
          "places": {
            "gte": form.people.data
          }
        }
      })

    # default sorting (most relevant)
    u_sort = ["_score", "username.raw"]
    t_sort = ["_score", "title.raw"]

    if form.sort_by.data == "Nearest to location":
      if location_sort:
        t_sort = [{"_geo_distance": {
          "destinations.location": {"lat":form.lat.data, "lon":form.lng.data},
          "mode":"min",
          "nested":{"path":"destinations"}
        }}, "_score"]
      else:
        flash("Location must be specified in order to sort for nearest distances.", "danger")
    elif form.sort_by.data == "Alphabetically, A-Z":
      u_sort = ["username.raw"]
      t_sort = ["title.raw", "description.raw", "_score"]
    elif form.sort_by.data == "Alphabetically, Z-A":
      u_sort = [{"username.raw": "desc"}]
      t_sort = [{"title.raw": "desc"}, {"description.raw": "desc"}, "_score"]
    elif form.sort_by.data == "Created, new to old":
      t_sort = ["created", "_score"]
    elif form.sort_by.data == "Created, old to new":
      t_sort = [{"created": "desc"}, "_score"]

    trips, dest = Trip.search(t_query, t_sort, dest=True)
    users = User.search(u_query, u_sort)

    filtered = bool(dest)

    if dest: dest = [d.to_json() for d in dest]
    else: dest = [[d.to_json() for d in t.destinations.all()] for t in trips.all()]
    
    trip_ids = {t.id : [d.to_json() for d in t.destinations.all() ] for t in trips.all()}

    trips = trips.paginate(page, form.results_per_page.data, error_out=False)
    users = users.paginate(page, form.results_per_page.data, error_out=False)

    args = dict(request.args)
    args.pop("page", None)
    args.pop("tab", None)

    return render_template("main/search.html", form=form, trips=trips, users=users, trip_ids=trip_ids,\
      query=args, dest={"dest":dest, "filtered":filtered})
  
  return render_template("main/search.html", form=form)


@sitemap.register_generator
def index(): yield "home.index", {}