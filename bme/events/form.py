from sqlite3 import Date
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired


#The form that allows users to post an event
class PostEventForm(FlaskForm):
    title = StringField("Title", validators = [DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    image = FileField("Add/Change Poster", validators=[FileAllowed(['jpg', 'png'])])
    date = DateField("Event Date", validators=[])

    submit = SubmitField("Post Event")

