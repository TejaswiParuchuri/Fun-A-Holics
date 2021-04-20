from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms_components import DateTimeField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from fun_a_holics.models import User
from fun_a_holics import current_user
from db_operations import dbconnection

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    age = IntegerField('Age', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    '''def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')'''


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

    event_name = StringField('Event Name', validators=[DataRequired()])
    event_description = TextAreaField('Description', validators=[
                                      DataRequired(), Length(min=2, max=500)])
    event_category = SelectField(
        u'Category', choices=categories, validators=[DataRequired()])
    start_date = DateTimeField('Start Date',
        format='%m/%d/%Y',
        validators = [DataRequired()],
        description = 'Time that the event will occur'
    )
    submit = SubmitField('Post Event')
