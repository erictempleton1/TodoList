import datetime
from todo import db
from werkzeug import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    signup_date = db.Column(db.DateTime)
    pw_hash = db.Column(db.String(64))
    user_list = db.relationship('UserTodo', backref = 'user', lazy = 'dynamic')

    def __init__(self, name, email, password):
        self.name = name.title()
        self.email = email.lower()
        self.signup_date = datetime.datetime.now()
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def __repr__(self):
        return '<User %r>' % (self.name)

class UserTodo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    todo_item = db.Column(db.String)
    item_due_date = db.Column(db.String(10))
    todo_item_note = db.Column(db.String(300))
    create_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<UserTodo %r>' % (self.todo_item)
    
    
    
      