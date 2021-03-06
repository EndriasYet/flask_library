from flask_wtf import Form
from flask import request
from wtforms import StringField, PasswordField, validators


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=5)]
                           # [validators.Length(min=1, max=50, message='Space can not be left empty'),
                           #  validators.InputRequired()]
                           )
    password = PasswordField('Password', [validators.Length(min=5),
                                          validators.DataRequired()])


def check_this_login(form):

    if isinstance(form, LoginForm):
        username = str(request.form['username'])
        password = str(request.form['password'])
        return [username, password]


def btn_login(form):
    if isinstance(form, LoginForm):
        if request.form["btn"] == "Log-in":
            return True
    else:
        return False
