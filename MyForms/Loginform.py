from flask_wtf import Form
from wtforms import StringField, PasswordField, validators


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=5)]
                           # [validators.Length(min=1, max=50, message='Space can not be left empty'),
                           #  validators.InputRequired()]
                           )
    password = PasswordField('Password', [validators.Length(min=5),
                                          validators.DataRequired()])


class SignupForm(Form):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=5)]
                           # [validators.Length(min=1, max=50, message='Space can not be left empty'),
                           #  validators.InputRequired()]
                           )
    password = PasswordField('Password', [validators.Length(min=5),
                                          validators.DataRequired()])
    password2 = PasswordField('Repeat Password', [validators.Length(min=5),
                                                  validators.DataRequired()])

