from flask import Flask, url_for, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from MyForms.check_this_book import *
from MyForms.check_this_login import *

app = Flask("__name__")
app.config['SECRET_KEY'] = 'BlahBlahBlah'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_site.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


class Books(db.Model):
    __tablename__ = "Books"
    isbn = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), unique=False, nullable=False)
    description = db.Column(db.String(30), unique=False, nullable=False)
    edition = db.Column(db.Integer, unique=False, nullable=True)
    published = db.Column(db.Integer, unique=False, nullable=True)
    category = db.Column(db.String(30), nullable=True, unique=False)

    def __repr__(self):
        return f"Books('{self.isbn}','{self.name}','{self.description}')"


class User(db.Model):
    __tablename__ = "Users"
    username = db.Column(db.String(), primary_key=True, nullable=False)
    password = db.Column(db.String(), unique=False, nullable=False)

    def __repr__(self):
        return f"Users('{self.username}','{self.password}')"


db.create_all()


# A login page that also works as a signing up page depending if a user has been registered or not
@app.route('/', methods=['GET', 'POST'])
def login():
    error = False
    # Search if a user exists and if it returns false create a register form and if true create a login form
    user = User.query.first()
    if user:
        form = LoginForm()
        empty = False
    else:
        form = SignupForm()
        empty = True

    if request.method == 'POST':
        # check the form and collect the data entered
        out = check_this_login(form)
        # if a user doesn't exist and a sign up form is completed then register the user
        if empty and btn_is_signup(form):
            # check if passwords match
            if out[1] == out[2]:
                # if passwords match create a user and store it in the database. Print 'added a new user'
                empty = False
                user = User(username=out[0], password=out[1])
                db.session.add(user)
                db.session.commit()
                print('Added a user')
            else:
                # if passwords don't match then return an error string
                error = "Passwords don't match. Please try again"
        # if user exists and log-in form is completed:
        elif (not empty) and btn_login(form):
            print('clicked login')
            # check if the user exists in the database
            if str(user.username) == out[0] and str(user.password) == out[1]:
                # if the entry is registered, start a session for the username and redirect to the home page
                print('user redirect')
                session['users'] = out[0]
                return redirect(url_for('books'))
            else:
                error = "Passwords and username don't match. Please try again"
        # if all of the conditionals return false then output a string. Used for debugging
        else:
            print('Fix something')
    return render_template('loginForm.html', form=form, error=error, empty=empty)


@app.route("/books", methods=['GET', 'POST'])
def books():
    success = False
    msg = ''
    detail = False
    error = ''
    # create a book-form object
    form = BookForm()
    user = User.query.first()

    # check if a session is under way for a user
    if not session.get("users") is None and user is not None:
        user.username = session['users']
        print('Stared')

        if request.method == 'POST':
            # check if the entry of the form is valid
            if book_is_valid(form):
                # out put the form entries into a list to parse
                ret = check_this_book(form)
                # create a book object based on the parsed data
                book = Books(name=ret[0], isbn=ret[1], description=ret[2], edition=ret[3], category=ret[4],
                             published=ret[5])
                print('Created Book')

                if btn_is_add(form):
                    # if the add button is pressed add the book to the database. If the data is incorrect raise an error
                    try:
                        db.session.add(book)
                        db.session.commit()
                        print('Added a Book')
                        success = True
                        msg = return_tile(form, 'added')
                    except IntegrityError:
                        db.session.rollback()
                        error = "Book with the same ISBN exists"
                        print(msg)

                else:
                    # if the pressed button is delete or get info. Search for a book with the same isbn(gets priority)
                    book = Books.query.filter_by(isbn=ret[1]).first()
                    if book and btn_is_remove(form):
                        # if book exists and the remove button is pressed Delete the book and return a confirmation
                        success = True
                        db.session.delete(book)
                        db.session.commit()
                        print('Deleted')
                        msg = return_tile(form, 'deleted')

                    elif book and btn_is_get(form):
                        # if the get_info button is pressed. Parse all the book data and return it to the html to
                        # display
                        print('Retrieving data')
                        detail = [book.name, book.isbn, book.description, book.edition, book.category, book.published]
                        msg = 'The Information available for the book you requested is:'

                    if book is None:
                        # if the book object with the same isbn doesn't exist then return an error string
                        success = False
                        error = "Can't find the book you requested"
            else:
                # if the book form entries are not valid, return an error string and print the errors for debugging
                error = "ERROR!! Empty ISBN or Title field detected. Please try again"
                print(form.errors)
        return render_template('home.html', form=form, success=success, msg=msg, error=error, detail=detail,
                               name=str(user.username))
    else:
        # if a user is not registered in the session return to the login page
        print("can't find user")
        return redirect(url_for('login'))

