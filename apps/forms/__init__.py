from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, TextAreaField, \
                    IntegerField, SelectMultipleField, PasswordField, \
                    validators, SubmitField, DateTimeField, FloatField
from wtforms.validators import Email, DataRequired, ValidationError, Length, Regexp

from apps.models_db import Users