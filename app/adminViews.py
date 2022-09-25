from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_login import current_user
from flask import abort


class IndexView(AdminIndexView):
  def is_accessible(self):
    return current_user.is_authenticated and current_user.admin

  def inaccessible_callback(self, name, **kwargs):
    return abort(403)


class UserView(ModelView):
  can_create = False
  can_view_details = True
  can_set_page_size = True
  column_list = ["uid", "username", "email", "first_name", "last_name", "created", "confirmed", "donator"]
  column_searchable_list = ["uid", "username", "email"]

  def is_accessible(self):
    return current_user.is_authenticated and current_user.admin

  def inaccessible_callback(self, name, **kwargs):
    return abort(403)


class TripView(ModelView):
  can_create = False
  can_view_details = True
  can_set_page_size = True
  column_list = ["uid", "title", "places", "created", "skipper"]
  column_searchable_list = ["uid", "title"]

  form_choices = {
    "boat_type": [
      ("Sailingboat", "Sailingboat"),
      ("Motorboat", "Motorboat")
    ],
    "sailing_mode": [
      ("Costal", "Costal"),
      ("Offshore", "Offshore"),
      ("Regatta", "Regatta"),
      ("Boat Delivery", "Boat Delivery")
    ]
  }

  def is_accessible(self):
    return current_user.is_authenticated and current_user.admin

  def inaccessible_callback(self, name, **kwargs):
    return abort(403)


class MessageView(ModelView):
  can_create = False
  can_edit = False
  can_view_details = True
  can_set_page_size = True
  column_list = ["uid", "subject", "created", "read", "sender", "receiver"]
  column_searchable_list = ["uid", "subject"]

  def is_accessible(self):
    return current_user.is_authenticated and current_user.admin

  def inaccessible_callback(self, name, **kwargs):
    return abort(403)


class UserMsgView(ModelView):
  can_create = False
  can_edit = False
  can_view_details = True
  can_set_page_size = True
  column_list = ["uid", "email", "created", "user"]
  column_searchable_list = ["uid", "email", "message"]

  def is_accessible(self):
    return current_user.is_authenticated and current_user.admin

  def inaccessible_callback(self, name, **kwargs):
    return abort(403)