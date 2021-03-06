from flask.ext.wtf import Form
from wtforms import TextField, validators, ValidationError, PasswordField, BooleanField, DateField
from models import db, User, UserTodo

class Signup(Form):
    name = TextField('Name', [validators.Required('Please enter your name')])
    email = TextField('Email', [validators.Required('Please enter your email'), validators.Email('Please enter a valid email address')])
    password = PasswordField('Password', [validators.Required('Please choose a password')])

class UserLogin(Form):
    email = TextField('email', [validators.Required('Please enter your email address'), validators.Email('Please enter a valid email address')])
    password = PasswordField('password', [validators.Required('Please enter your password')])
    remember_me = BooleanField('remember_me', default=False)

class TodoList(Form):
    todo_item = TextField('todo_item', [validators.Required('Please enter an item for your list!')])
    item_note = TextField('item_note')
    due_date = DateField('due_date', [validators.Required('Please choose a due date (eg: 3/14/2014)')], format='%m/%d/%Y')

class UpdateList(Form):
    todo_item = TextField('todo_item', [validators.Required('Please enter an item for your list your list!')])
    due_date = DateField('due_date', [validators.Required('Please choose a due date (eg: 3/15/2014)')], format='%m/%d/%Y')

class SearchList(Form):
    search_item = TextField('search_item', [validators.Required('Please enter a word to search for!')])
    