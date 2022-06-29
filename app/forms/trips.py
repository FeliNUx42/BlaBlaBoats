from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, DateField, SelectField, SubmitField, FileField, FieldList, FormField, HiddenField, DecimalField
from wtforms.validators import DataRequired, Length, Optional
from flask_wtf.file import FileAllowed


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


class DeleteTrip(FlaskForm):
  submit = SubmitField("Yes")


class AddImage(FlaskForm):
  image = FileField(label="Image", validators=[DataRequired(), FileAllowed(["jpg", "png", "jpeg"], "Only images are accepted!")])
  add_submit = SubmitField("Add Image")


class DeleteImage(FlaskForm):
  image = HiddenField(label="Image", validators=[DataRequired()])
  del_submit = SubmitField("Delete this Image")