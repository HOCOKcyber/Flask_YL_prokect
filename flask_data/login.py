from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('Ваш ник в игре:', validators=[DataRequired()])
    submit = SubmitField('Войти')
