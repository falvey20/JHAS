from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from blog.models import User


class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    email = EmailField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6, max=30), EqualTo('password')])
    
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, please choose another!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already in use, use another or sign in.')

class LoginForm(FlaskForm):

    email = EmailField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    email = EmailField('Email', validators=[DataRequired(), Email()])
    
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken, please choose another!')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already in use, use another or sign in.')

class AddMixForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content_link = StringField('Link', validators=[DataRequired()])
    content = TextAreaField('Notes (optional)')
    theme = SelectField('Theme (optional)', coerce=int, choices=[(0, 'Unselected'), (1, 'Bangers'), (2, 'Ambient'), (3, 'Gym'), (4, 'Chilled'), (5, 'Work'), (6, 'Sleep'), (7, 'Meditation'), (8, 'Party')])
    submit = SubmitField('Add')


class RequestResetForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email, go ahead and register!')

#RESET PASSWORD FORM
class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6, max=30)])

    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), Length(min=6, max=30), EqualTo('password')])

    submit = SubmitField('Reset Password')



            