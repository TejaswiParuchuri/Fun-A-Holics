from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from fun_a_holics.models import User
from fun_a_holics import current_user
from db_operations import dbconnection
from wtforms.fields.html5 import DateTimeLocalField
from datetime import datetime

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    age = IntegerField('Age', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    age = IntegerField('Age', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[
        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')



class EventForm(FlaskForm):
    categories = ["hiking", "boating", "art",
                  "movies", "games", "fitness", "dance","other"]
    criterias = ["indoor", "outdoor"]
    event_name = StringField('Event Name', validators=[DataRequired(),Length(min=2, max=100)], description='Event name')
    event_description = TextAreaField('Description', validators=[
                                      DataRequired(), Length(min=2, max=500)], description='Describe your event here')
    event_category = SelectField(
        u'Category', choices=categories, validators=[DataRequired()])
    start_date = DateTimeLocalField('Start Date', default=datetime.now, format='%Y-%m-%dT%H:%M')
    end_date  = DateTimeLocalField('End Date', default=datetime.now, format='%Y-%m-%dT%H:%M')
    cost_per_person = IntegerField('Cost per person', validators=[], default=0)
    link_to_connect = StringField('Link to Connect', validators=[Length(min=2, max=500)])
    max_capacity = IntegerField('Capacity', validators=[DataRequired(), NumberRange(min=2, max=50, message="capacity between 2 to 50")])
    location = StringField('Location', validators=[Length(min=2, max=500)], default="Indoor")
    criteria  = SelectField(
        u'Criteria ', choices=criterias , validators=[DataRequired()])
    min_age = IntegerField('Min age', validators=[DataRequired(), NumberRange(min=10, message="Min age is 10 years")])
    max_age = IntegerField('Max age', validators=[DataRequired(), NumberRange(max=60, message="Max age is 60 years")])
    event_city =  StringField('Event City', validators=[Length(min=2, max=10)])
    event_state  =  StringField('Event State', validators=[Length(min=2, max=10)])
    covid_test =  BooleanField('Covid test required')
    submit = SubmitField('Post Event')
