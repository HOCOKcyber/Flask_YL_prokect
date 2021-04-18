from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class DonateForm(FlaskForm):
    user_name = StringField('Ваш ник (в игре)', validators=[DataRequired()])
    donate = StringField('Донат (1 руб. = 50 кликер)', validators=[DataRequired()])
    submit = SubmitField('Оплатить')
