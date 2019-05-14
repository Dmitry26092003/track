from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
 
class AddDishForm(FlaskForm):
    title = StringField('Название рецепта', validators=[DataRequired()])
    content = TextAreaField('Содержание рецепта', validators=[DataRequired()])
    submit = SubmitField('Добавить')