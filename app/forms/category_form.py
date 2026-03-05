from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CategoryForm(FlaskForm):
    name = StringField("Category Name", validators=[DataRequired()])
    image = StringField("Image URL")
    submit = SubmitField("Submit")