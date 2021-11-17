"""Models for Feeback app """

from flask import session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def connect_db(app):
    """ Connect to database """

    db.app = app
    db.init_app(app)


def authorize(username):
    """ Verify that logged in user is same as target user """
    if session['username'] != username:
        return False
    else:
        return True


class User(db.Model):

    __tablename__ = 'users'

    username = db.Column( db.String(20), primary_key=True)
    password = db.Column( db.Text, nullable = False )
    email = db.Column( db.String(50), unique = True, nullable=False )
    first_name = db.Column( db.String(30), nullable = False )
    last_name = db.Column( db.String(30), nullable = False )

    feedback = db.relationship('Feedback', backref='users')

    def __repr__(self):
        user = self
        return f'<User {user.username}>'

    @classmethod
    def register(cls, username, pwd, email, fname, lname):
        """ Create and return new user """

        bcrypt = Bcrypt()

        hashed_pwd = bcrypt.generate_password_hash(pwd)
        hashed_pwd_utf8 = hashed_pwd.decode('utf8')

        return cls(username=username, password=hashed_pwd_utf8, email=email, first_name=fname, last_name=lname)

    @classmethod
    def authenticate(cls, username, pwd):
        """ Validate that user exists & password is correct. Return user if valid; else return False. """

        bcrypt = Bcrypt()
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False


class Feedback(db.Model):

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'))
