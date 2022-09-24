from xml.dom import ValidationErr
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_wtf.file import FileAllowed
from app.models import User


class SettingsForm(FlaskForm):
  username = StringField(label="Username", validators=[DataRequired(), Length(4, 128)], default=lambda: current_user.username)
  description = TextAreaField(label="User description", validators=[DataRequired(), Length(0, 1024)], default=lambda: current_user.description)
  picture = FileField(label="Profile Picture", validators=[FileAllowed(["jpg", "png", "jpeg"], "Only images are accepted!")])
  first_name = StringField(label="First Name", validators=[DataRequired(), Length(4, 128)], default=lambda: current_user.first_name)
  last_name = StringField(label="Last Name", validators=[DataRequired(), Length(4, 128)], default=lambda: current_user.last_name)
  submit = SubmitField("Save changes")

  def validate_username(self, username):
    if username.data == current_user.username: return
    if not User.query.filter_by(username=username.data).first(): return
    
    raise ValidationError("Already taken.")
  