from flask_wtf import FlaskForm
from wtforms import SubmitField


class NavBarForm(FlaskForm):
    submit = SubmitField('Войти')
