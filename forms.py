""" Forms for the Feedback app """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import InputRequired, Length, Email


class NewUserForm(FlaskForm):

    first_name = StringField('First Name', 
        validators=[InputRequired(), Length(max=30, message='Limit 30 characters')])
    last_name = StringField('Last Name', 
        validators=[InputRequired(), Length(max=30, message='Limit 30 characters')])
    email = StringField('Email Address', 
        validators=[InputRequired(), Email(message="Not a valid email address"), 
                    Length(max=50, message='Limit 50 characters')])
    username = StringField('Username', 
        validators=[InputRequired(), Length(max=20, message='Limit 20 characters')])
    password = PasswordField('Password', validators=[InputRequired()])


class LoginForm(FlaskForm):

    username = StringField('Username', 
        validators=[InputRequired(), Length(max=20, message='Limit 20 characters')])
    password = PasswordField('Password', validators=[InputRequired()])


class EditFeedbackForm(FlaskForm):

    title = StringField('Title', validators=[InputRequired(), Length(max=100, message='Limit 100 characters')])
    content = TextAreaField('Content', validators=[InputRequired()])
    
    
