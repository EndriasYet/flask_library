from flask_wtf import Form
from flask import request
from wtforms import StringField, PasswordField, validators


class SignupForm(Form):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=5)]
                           # [validators.Length(min=1, max=50, message='Space can not be left empty'),
                           #  validators.InputRequired()]
                           )
    password = PasswordField('Password', [validators.Length(min=5),
                                          validators.DataRequired()])
    password2 = PasswordField('Repeat Password', [validators.Length(min=5),
                                                  validators.DataRequired()])


def check_this_signup(form):

    if isinstance(form, SignupForm):
        username = str(request.form['username'])
        password = str(request.form['password'])
        password2 = str(request.form['password2'])
        return [username, password, password2]
    else:
        return False


def btn_is_signup(form):
    if isinstance(form, SignupForm):
        if request.form["btn"] == "Sign-up":
            return True
    else:
        return False


def passwords_match():
    if request.form['password'] == request.form['password2']:
        return True
    else:
        return False
