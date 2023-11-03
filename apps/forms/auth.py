from . import datetime
from . import FlaskForm
from . import BooleanField, StringField, TextAreaField, \
                    IntegerField, SelectMultipleField, PasswordField, \
                    validators, SubmitField, DateTimeField, FloatField
from . import Email, DataRequired, ValidationError,Length, Regexp

from . import Users

class LoginForm(FlaskForm):
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired(),Length(3, 128)])
    
    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('User does not exist')



class CreateAccountForm(FlaskForm):
    username = StringField('Username',
                         id='username_create',
                         validators=[
                            DataRequired(),  
                            Length(3, 20, message="Please provide a valid name"), 
                            Regexp("^[A-Za-z][A-Za-z0-9_.]*$",
                                   0,
                                    "Usernames must have only letters, " "numbers, dots or underscores",
                                ),
                            ]
                        )
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email(), Length(3, 128)])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
    
    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username exists, please pick another one')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email exists, please pick another one')


