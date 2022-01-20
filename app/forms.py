from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, DateField, SubmitField 
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo
from .models import User


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
  first_name = StringField(label="First Name:", validators=[DataRequired(), Length(4, 128)], default=lambda: current_user.first_name)
  last_name = StringField(label="Last Name:", validators=[DataRequired(), Length(4, 128)], default=lambda: current_user.last_name)
  birthday = DateField("Date of birth:", validators=[DataRequired()], default=lambda: current_user.birthday)
  
  submit = SubmitField("Save changes")

class ChangePasswordForm(FlaskForm):
  o_password = PasswordField(label="Old Password:", validators=[DataRequired(), Length(8, 128)])
  n_password = PasswordField(label="New Password:", validators=[DataRequired(), Length(8, 128)])
  r_password = PasswordField(label="Repeate New Password:", validators=[DataRequired(), EqualTo("n_password"), Length(8, 128)])
  submit = SubmitField("Change Password")
