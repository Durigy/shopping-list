from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp, InputRequired, NumberRange, Email
from main.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username *', validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField('Email *', validators=[DataRequired(), Email()])
    password = PasswordField('Password *', validators=[DataRequired()]) #, Regexp('^(?=.*\d).{6,20}$', message='Your password should be between 6 and 20 Charaters long and contain at least 1 number')])
    confirm_password = PasswordField('Confirm Password *', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already Taken. Please choose a different one.')

    def validate_email(self, email):
       email = User.query.filter_by(email=email.data).first()
       if email:
           raise ValidationError('Email already Used. Please Use a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password', validators=[DataRequired()]) #, Regexp('^(?=.*\d).{6,20}$', message='Your password should be between 6 and 20 Charaters long and contain at least 1 number')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username *', validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField('Email *', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Account')

    def validate_username(self, username):
        if username.data.lower() != current_user.username.lower():
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already Taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email already Used. Please Use a different one.')

class AddListForm(FlaskForm):
    name = StringField('Shopping List Name *', validators=[DataRequired()])
    submit = SubmitField('Create List')

class UpdateListForm(FlaskForm):
    list_name = StringField('Shopping List Name *', validators=[DataRequired()])
    submit = SubmitField('Updata List')

class AddListItemForm(FlaskForm):
    name = StringField('Item Name *', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[NumberRange(min=1)])
    submit = SubmitField('Update Item')