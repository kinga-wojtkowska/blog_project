from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired
from blog.models import Entry


class EntryForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    body = TextAreaField('Wpis', validators=[DataRequired()])
    is_published = BooleanField('Publikujemy?')