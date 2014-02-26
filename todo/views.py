from flask import render_template, request, flash, redirect
from forms import Signup
from models import User
from todo import app, db

@app.route('/')
def index():
    return render_template('base.html', title='Home')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Signup()

    if request.method == 'POST' and form.validate() == False:
        return render_template('signup.html', form=form, title='Signup')
    elif request.method == 'GET':
        return render_template('signup.html', form=form, title='Signup')
    else:
        newuser = User(form.name.data, form.email.data, form.password.data)
        db.session.add(newuser)
        db.session.commit()
        return redirect('/')