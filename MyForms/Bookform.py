from flask_wtf import Form
from flask import request
from wtforms import StringField, IntegerField, SubmitField, PasswordField, validators, TextAreaField
from wtforms.validators import DataRequired, InputRequired,Length, NumberRange, Optional


class BookForm(Form):
    name = StringField('Title:'
                       # [validators.Length(min=1, max=50, message='Space can not be left empty'),
                       #  validators.InputRequired()]
                       )
    isbn = IntegerField('ISBN Id(13 digits long)',
                         [validators.Length(min=13, max=13, message='ISBN must be 13digits long')]
                        )
    description = TextAreaField('Description:')
    edition = IntegerField('Edition:', [validators.length(min=0, max=20), validators.optional()])
    category = StringField('Category:', [validators.length(min=0, max=20), validators.optional()])
    year = IntegerField('Published:', [validators.NumberRange(min=0, max=2024),
                                                                      validators.optional()])


def check_this_book(form):
    if isinstance(form, BookForm):
        name = str(request.form['name'])
        isbn = int(request.form['isbn'])
        description = str(request.form['edition']) if len(str(request.form['description'])) != 0 else "-"
        edition = int(request.form['edition']) if len(str(request.form['description'])) != 0 else "-"
        category = str(request.form['category']) if len(str(request.form['description'])) != 0 else "-"
        year = int(request.form['year']) if len(str(request.form['year'])) != 0 else "-"
        return [name, isbn, description, edition, category, year]
    else:
        return False


def book_is_valid(form):
    if isinstance(form, BookForm):
        if len(request.form['isbn']) == 13 and len(request.form['name']) != 0:
            return True
        else:
            return False
    else:
        return False


def btn_is_add(form):
    if isinstance(form, BookForm):
        if request.form["btn"] == "Add-Book":
            return True
    else:
        return False


def btn_is_remove(form):
    if isinstance(form, BookForm):
        if request.form["btn"] == "Remove-Book":
            return True
    else:
        return False


def btn_is_get(form):
    if isinstance(form, BookForm):
        if request.form["btn"] == "Get-Info":
            return True
    else:
        return False


def return_tile(form, act):
    if isinstance(form, BookForm):
        return "Successfully " + act + request.form['name'] + "(ISBN:" + request.form[
            'isbn'] + ")" + " to your library"
    else:
        return False
