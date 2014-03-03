from flask.ext.wtf import Form
from wtforms import TextField, validators, ValidationError, PasswordField, BooleanField
from models import db, User

class Signup(Form):
    name = TextField('Name', [validators.Required('Please enter your name')])
    email = TextField('Email', [validators.Required('Please enter your email'), validators.Email('Please enter a valid email address')])
    password = PasswordField('Password', [validators.Required('Please choose a password')])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        if User.query.filter_by(email = self.email.data.lower()).count() > 0:
            self.email.errors.append('Email already in use.')
            return False
        else:
            return True

class UserLogin(Form):
    email = TextField('email', [validators.Required('Please enter your email address'), validators.Email('Please enter a valid email address')])
    password = PasswordField('password', [validators.Required('Please enter your password')])
    remember_me = BooleanField('remember_me', default=False)