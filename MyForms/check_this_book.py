from flask import request
from MyForms.Bookform import BookForm


def check_this_book(form):
    if isinstance(form, BookForm):
        name = str(request.form['name'])
        isbn = int(request.form['isbn'])
        description = str(request.form['edition']) if len(str(request.form['description'])) is None else ""
        edition = int(request.form['edition']) if len(str(request.form['description'])) is None else ""
        category = str(request.form['category']) if len(str(request.form['description'])) is None else ""
        year = int(request.form['year']) if len(str(request.form['year'])) is None else ""
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
