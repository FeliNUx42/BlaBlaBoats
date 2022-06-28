from flask import request
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, PasswordField, BooleanField, DateField, SelectField, SubmitField, FileField, FieldList, FormField, HiddenField, DecimalField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo, Optional, NumberRange
from flask_wtf.file import FileRequired, FileAllowed
from .models import User


class SearchForm(FlaskForm):
  q = StringField("Search", validators=[Optional()])
  lat = DecimalField(validators=[Optional()])
  lng = DecimalField(validators=[Optional()])
  dist = IntegerField(label="Max. distance to location", validators=[Optional(), NumberRange(min=0, max=3000)])
  unit = SelectField(choices=("km", "mi", "nmi"), validators=[DataRequired()])
  start_date = DateField(validators=[Optional()])
  end_date = DateField(validators=[Optional()])
  boat_type = SelectField(label="Boat type", choices=("All", "Sailingboat", "Motorboat"), validators=[DataRequired()])
  sailing_mode = SelectField(label="Sailing mode", choices=("All", "Costal", "Offshore", "Regatta", "Boat Delivery"), validators=[DataRequired()])
  sort_by = SelectField(label="Sort by", choices=("Most relevant", "Nearest to location", "Alphabetically, A-Z", "Alphabetically, Z-A", "Created, new to old", "Created, old to new"), validators=[Optional()])
  results_per_page = IntegerField(label="Results per page", validators=[Optional(), NumberRange(min=0, max=100)], default=25)

  def __init__(self, *args, **kwargs):
    if 'formdata' not in kwargs:
      kwargs['formdata'] = request.args
    if 'meta' not in kwargs:
      kwargs['meta'] = {'csrf': False}
      super(SearchForm, self).__init__(*args, **kwargs)

class SignupForm(FlaskForm):
  username = StringField(label="Username:", validators=[DataRequired(), Length(4, 128)])
  email = StringField(label="Email Address:", validators=[DataRequired(), Email(), Length(6, 128)])
  first_name = StringField(label="First Name:", validators=[DataRequired(), Length(4, 128)])
  last_name = StringField(label="Last Name:", validators=[DataRequired(), Length(4, 128)])
  password = PasswordField(label="Password:", validators=[DataRequired(), Length(8, 128)])
  r_password = PasswordField(label="Repeate password:", validators=[DataRequired(), EqualTo("password"), Length(8, 128)])
  submit = SubmitField("Sign Up")

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError("This Username is already taken.")
  
  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError("This Email Address is already taken.")

class LoginForm(FlaskForm):
  username = StringField(label="Username:", validators=[DataRequired(), Length(4, 128)])
  password = PasswordField("Password:", validators=[DataRequired(), Length(8, 128)])
  remember = BooleanField("Remember me")
  submit = SubmitField("Log In")

class SettingsForm(FlaskForm):
  username = StringField(label="Username:", validators=[DataRequired(), Length(4, 128)], default=lambda: current_user.username)
  description = TextAreaField(label="User description:", validators=[DataRequired(), Length(0, 1024)], default=lambda: current_user.description)
  picture = FileField(label="Profile Picture", validators=[FileAllowed(["jpg", "png", "jpeg"], "Only images are accepted!")])
  first_name = StringField(label="First Name:", validators=[DataRequired(), Length(4, 128)], default=lambda: current_user.first_name)
  last_name = StringField(label="Last Name:", validators=[DataRequired(), Length(4, 128)], default=lambda: current_user.last_name)
  #birthday = DateField("Date of birth:", validators=[Optional()], default=lambda: current_user.birthday)
  submit = SubmitField("Save changes")

class ChangePasswordForm(FlaskForm):
  o_password = PasswordField(label="Old Password:", validators=[DataRequired(), Length(8, 128)])
  n_password = PasswordField(label="New Password:", validators=[DataRequired(), Length(8, 128)])
  r_password = PasswordField(label="Repeate New Password:", validators=[DataRequired(), EqualTo("n_password"), Length(8, 128)])
  submit = SubmitField("Change Password")

class Place(Form):
  place = StringField(label="Stopover", validators=[Length(max=64)])
  lat = DecimalField(label="Latitude", validators=[Optional()])
  lng = DecimalField(label="Longitude", validators=[Optional()])
  arr_date = DateField(label="Date of arrival", validators=[Optional()])
  dep_date = DateField(label="Date of departure", validators=[Optional()])

class CreateEditTripForm(FlaskForm):
  title = StringField(label="Title", validators=[DataRequired(), Length(max=72)])
  banner = FileField(label="Banner Image", validators=[FileAllowed(["jpg", "png", "jpeg"], "Only images are accepted!")])
  description = TextAreaField(label="Description", validators=[DataRequired(), Length(max=2048)])
  dest = FieldList(FormField(Place), label="Destinations", min_entries=2, max_entries=50)
  boat_type = SelectField(label="Boat type", choices=("Sailingboat", "Motorboat"), validators=[DataRequired()])
  boat_model = StringField(label="Boat model", validators=[DataRequired(), Length(max=10)])
  sailing_mode = SelectField(label="Sailing mode", choices=("Costal", "Offshore", "Regatta", "Boat Delivery"), validators=[DataRequired()])
  travel_expenses = StringField(label="Travel expenses", validators=[DataRequired(), Length(max=64)])
  qualif_level = StringField(label="Qualification level required", validators=[DataRequired(), Length(max=64)])
  submit = SubmitField("Create Trip")

class MsgContactForm(FlaskForm):
  subject = StringField(label="Subject", validators=[DataRequired(), Length(max=64)])
  content = TextAreaField(label="Content", validators=[DataRequired(), Length(max=2048)])
  u_uid = HiddenField(label="U_UID", validators=[DataRequired(), Length(16, 16)])
  submit = SubmitField("Send Message")

class MsgAboutForm(FlaskForm):
  subject = StringField(label="Subject", validators=[DataRequired(), Length(max=64)])
  content = TextAreaField(label="Content", validators=[DataRequired(), Length(max=2048)])
  t_uid = HiddenField(label="T_UID", validators=[DataRequired(), Length(16, 16)])
  submit = SubmitField("Send Message")

class MsgReplyForm(FlaskForm):
  content = TextAreaField(label="Content", validators=[DataRequired(), Length(max=2048)])
  r_uid = HiddenField(label="R_UID", validators=[DataRequired(), Length(16, 16)])
  submit = SubmitField("Send Message")

class AddImage(FlaskForm):
  image = FileField(label="Image", validators=[DataRequired(), FileAllowed(["jpg", "png", "jpeg"], "Only images are accepted!")])
  add_submit = SubmitField("Add Image")

class DeleteImage(FlaskForm):
  image = HiddenField(label="Image", validators=[DataRequired()])
  del_submit = SubmitField("Delete this Image")

class DonateForm(FlaskForm):
  amount = DecimalField(label="Amount", validators=[DataRequired(), NumberRange(1)])
  submit = SubmitField("Donate")