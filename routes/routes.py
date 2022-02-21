import logging
from flask import Flask, url_for, redirect, render_template, session
from Database.database import db, User, Books
from sqlalchemy.exc import IntegrityError
from MyForms.Bookform import *
from MyForms.Loginform import *
from MyForms.Signupform import *

app = Flask("__name__")
app.config['SECRET_KEY'] = 'BlahBlahBlah'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_site.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db.app = app
db.init_app(app)
db.create_all()


# A landing page for the customer to sign up or log in
@app.route('/', methods=['GET', 'POST'])
def home():
    msg = False
    if request.method == 'POST':
        if request.form["btn"] == "Sign-Up":
            return redirect(url_for('signup'))
        elif request.form["btn"] == "Log-in":
            return redirect(url_for('login'))
        elif request.form["btn"] == "About Library":
            msg = "This online library tool is intended for customers to store and remove books in their current " \
                  "physical " \
                  "library so that they can track their library remotely. \n Created: Jan-2022 by Endriase Yetbark \n" \
                  " Last-modifications: Feb-2022(added a server to store the data rather than save it locally \n"
            msg = msg.split('\n')
    return render_template('landing.html', msg=msg)


# A login page that also works as a signing up page depending if a user has been registered or not
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    error=False
    if request.method == 'POST':
        info = check_this_signup(form)
        if btn_is_signup(form):
            check_user = User.query.filter_by(username=info[0]).first()
            if check_user:  # User already exists
                error="Username already exists. Try another one"
            # check if passwords match
            elif passwords_match():
                # if passwords match create a user and store it in the database. Print 'added a new user'
                user = User(username=info[0], password=info[1])
                db.session.add(user)
                db.session.commit()
                print('Added a user')
                return redirect(url_for('login'))
            else:
                # if passwords don't match then return an error string
                error = "Passwords don't match. Please try again"
        # if user exists and log-in form is completed:
    return render_template('signupForm.html', form=form, error=error)


# A login page that also works as a signing up page depending if a user has been registered or not
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = False
    # Search if a user exists and if it returns false create a register form and if true create a login form
    if request.method == 'POST':
        # check the form and collect the data entered
        info = check_this_login(form)
        # if user exists and log-in form is completed:
        if btn_login(form):
            print('clicked login')
            user = User.query.filter_by(username=info[0]).first()
            # check if the user exists in the database
            if user is None:
                error = "Username doesn't exist. Try creating a new account"
            elif str(user.username) == info[0] and str(user.password) == info[1]:
                # if the entry is registered, start a session for the username and redirect to the home page
                print('user redirect')

                session['users'] = info[0]
                return redirect(url_for('books'))
            else:
                error = "Passwords and username don't match. Please try again"
        # if all of the conditionals return false then output a string. Used for debugging
        else:
            print('Fix something')
    return render_template('loginForm.html', form=form, error=error)


@app.route("/books", methods=['GET', 'POST'])
def books():
    success = detail = False
    msg = error = ''
    # create a book-form object
    form = BookForm()
    if len(session) == 0:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['users'])
    # query all books owned by the user to display on the web site
    # check if a session is under way for a user
    if  user is not None:
        user.username = session['users']
        print('Stared')
        print(user.username)
        displaybooks = Books.query.filter_by(owner=user.username).all()
        library = []
        for book in displaybooks:
            library.append([book.name, book.isbn, book.description, book.category, book.edition])
        print(library)
        if request.method == 'POST':
            # check if the entry of the form is valid
            if book_is_valid(form):
                # out put the form entries into a list to parse
                ret = check_this_book(form)
                # create a book object based on the parsed data
                book = Books(owner=user.username, name=ret[0], isbn=ret[1], description=ret[2], edition=ret[3],
                             category=ret[4],
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
                    except Exception as e:
                        db.session.rollback()
                        error = "Book with the same ISBN exists"
                        print((e))
                    return redirect(url_for('books'))

                else:
                    # if the pressed button is delete or get info. Search for a book with the same isbn(gets priority)
                    book = Books.query.filter_by(owner=user.username, isbn=ret[1]).first()
                    if book and btn_is_remove(form):
                        # if book exists and the remove button is pressed Delete the book and return a confirmation
                        success = True
                        db.session.delete(book)
                        db.session.commit()
                        print('Deleted')
                        msg = return_tile(form, 'deleted')
                        return redirect(url_for('books'))

                    elif book and btn_is_get(form):
                        # if the get_info button is pressed. Parse all the book data and return it to the html to
                        # display
                        print('Retrieving data')
                        detail = [book.name, book.isbn, book.description, book.edition, book.category, book.published]
                        msg = 'The Information available for the book you requested is:'

                    elif book is None:
                        # if the book object with the same isbn doesn't exist then return an error string
                        success = False
                        error = "Can't find the book you requested"
            else:
                # if the book form entries are not valid, return an error string and print the errors for debugging
                error = "ERROR!! Invalid ISBN or empty title field detected. Please try again"
                print(form.errors)
        return render_template('mainlibrary.html', form=form, success=success, msg=msg, error=error, detail=detail,
                               name=str(user.username), library=library)
    else:
        # if a user is not registered in the session return to the login page
        print("can't find user")
        return redirect(url_for('login'))
