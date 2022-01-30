from flask import request
from MyForms.Loginform import LoginForm, SignupForm


def check_this_login(form):

    if isinstance(form, LoginForm):
        username = str(request.form['username'])
        password = str(request.form['password'])
        return [username, password]

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


def btn_login(form):
    if isinstance(form, LoginForm):
        if request.form["btn"] == "Log-in":
            return True
    else:
        return False
