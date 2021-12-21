from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class FilterForm(FlaskForm):
    text = StringField('Text')
    from_date = StringField('From Date  - DD/MM/YY')
    to_date = StringField('To Date  - DD/MM/YY')
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    user_name = StringField('Twitter Username',
                        validators=[DataRequired()])
    submit = SubmitField('Submit')
