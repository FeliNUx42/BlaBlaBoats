from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, PasswordField, BooleanField, DateField, SelectField, SubmitField, FileField, FieldList, FormField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo, Optional
from flask_wtf.file import FileRequired, FileAllowed
from .models import User


class Place(Form):
  place = StringField(label="Stopover", validators=[Length(max=64)])
  arr_date = DateField(label="Date of arrival", validators=[Optional()])
  dep_date = DateField(label="Date of departure", validators=[Optional()])


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


class ContactForm(FlaskForm):
  subject = StringField(label="Subject", validators=[DataRequired(), Length(max=64)])
  content = TextAreaField(label="Content", validators=[DataRequired(), Length(max=2048)])
  submit = SubmitField("Send message")

class AddImage(FlaskForm):
  image = FileField(label="Image", validators=[DataRequired(), FileAllowed(["jpg", "png", "jpeg"], "Only images are accepted!")])
  add_submit = SubmitField("Add Image")

class DeleteImage(FlaskForm):
  image = HiddenField(label="Image", validators=[DataRequired()])
  del_submit = SubmitField("Delete this Image")