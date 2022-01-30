from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField, PasswordField, validators, TextAreaField
from wtforms.validators import DataRequired, InputRequired,Length, NumberRange, Optional


class BookForm(Form):
    name = StringField('Insert the title of the book'
                       # [validators.Length(min=1, max=50, message='Space can not be left empty'),
                       #  validators.InputRequired()]
                       )
    isbn = IntegerField('Insert the isbn id'
                        # [validators.Length(min=12, max=14, message='ISBN must be 13digits long')]
                        )
    description = TextAreaField('Type in the description of the book')
    edition = IntegerField('Insert the edition', [validators.length(min=0, max=20), validators.optional()])
    category = StringField('Type in the category', [validators.length(min=0, max=20), validators.optional()])
    year = IntegerField('Insert the year the book was published on', [validators.NumberRange(min=0, max=2024),
                                                                      validators.optional()])

