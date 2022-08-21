from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo
from app.models import User


class SignupForm(FlaskForm):
  username = StringField(label="Username:", validators=[DataRequired(), Length(4, 128)])
  email = StringField(label="Email Address:", validators=[DataRequired(), Email(), Length(6, 128)])
  first_name = StringField(label="First Name:", validators=[DataRequired(), Length(4, 128)])
  last_name = StringField(label="Last Name:", validators=[DataRequired(), Length(4, 128)])
  password = PasswordField(label="Password:", validators=[DataRequired(), Length(8, 128)])
  r_password = PasswordField(label="Repeat password:", validators=[DataRequired(), EqualTo("password"), Length(8, 128)])
  submit = SubmitField("Sign Up")

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError("This Username is already taken.")
  
  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError("This Email Address is already taken.")


class ConfirmForm(FlaskForm):
  submit = SubmitField("Resend Confirmation Email")


class  ResetRequestForm(FlaskForm):
  email = StringField("Email Address: ", validators=[DataRequired(), Email(), Length(4, 128)])
  submit = SubmitField("Reset Password")


class  ResetPasswordForm(FlaskForm):
  password = PasswordField(label="New Password:", validators=[DataRequired(), Length(8, 128)])
  r_password = PasswordField(label="Repeat password:", validators=[DataRequired(), EqualTo("password"), Length(8, 128)])
  submit = SubmitField("Save Password")


class LoginForm(FlaskForm):
  username = StringField(label="Username:", validators=[DataRequired(), Length(4, 128)])
  password = PasswordField("Password:", validators=[DataRequired(), Length(8, 128)])
  remember = BooleanField("Remember me")
  submit = SubmitField("Log In")

  def validate_password(self, password):
    user = User.query.filter_by(username=self.username.data).first()
    if not user or not user.verify_password(password.data):
      raise ValidationError("Wrong username or password.")


class ChangePasswordForm(FlaskForm):
  o_password = PasswordField(label="Old Password:", validators=[DataRequired(), Length(8, 128)])
  n_password = PasswordField(label="New Password:", validators=[DataRequired(), Length(8, 128)])
  r_password = PasswordField(label="Repeat New Password:", validators=[DataRequired(), EqualTo("n_password"), Length(8, 128)])
  submit = SubmitField("Change Password")

  def validate_o_password(self, o_password):
    if not current_user.verify_password(o_password.data):
      raise ValidationError("The old password doesn't match.")