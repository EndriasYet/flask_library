from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "User"
    username = db.Column(db.String(), primary_key=True, nullable=False)
    password = db.Column(db.String(), unique=False, nullable=False)

    def __repr__(self):
        return f"Users('{self.username}','{self.password}')"


class Books(db.Model):
    __tablename__ = "Books"
    owner = db.Column(db.String, db.ForeignKey('User.username'), nullable=False)
    isbn = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), unique=False, nullable=False)
    description = db.Column(db.String(30), unique=False, nullable=False)
    edition = db.Column(db.Integer, unique=False, nullable=True)
    published = db.Column(db.Integer, unique=False, nullable=True)
    category = db.Column(db.String(30), nullable=True, unique=False)

    def __repr__(self):
        return f"Books('{self.isbn}','{self.name}','{self.description}')"

# Server = 'DESKTOP-LNJG9L8\SQLEXPRESS'
# Database = 'Master'
# Driver = 'ODBC Driver 17for SQL Server'
# Connection_string = f'mssql://@{Server}/{Database}?driver={Driver}'
#
# engine = create_engine(Connection_string)
# con = engine.connect()