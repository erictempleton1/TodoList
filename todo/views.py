from flask import render_template, request, flash, redirect, url_for, session, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import Signup, UserLogin
from models import User
from todo import app, db, login_manager
from werkzeug.security import check_password_hash

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
def index():
    return render_template('base.html', title='Home')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Signup()

    if request.method == 'POST' and form.validate() == False or request.method == 'GET':
        return render_template('signup.html', form=form, title='Signup')

    else:
        newuser = User(form.name.data, form.email.data, form.password.data)
        db.session.add(newuser)
        db.session.commit()
        return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))

    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        email_submit = User.query.filter_by(email=form.email.data).first()
        pw_submit = User.query.filter_by(password=form.password.data).first()

    if email_submit is None:
        flash('Email already in use.')
        return redirect(url_for('login')

    if not pw_submit.check_password(pw_submit):
        flash('Invalid password')
        return redirect(url_for('login')
    login_user(email_submit, pw_submit)
    return redirect(url_for('index')
        

"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))

    form = UserLogin()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        user_check = User.query.filter_by(email=form.email.data, password=form.password.data).first()
        
        if user_check is not None:
            g.user = user_check
            login_user(user_check)
            return redirect('/')
    return render_template('login.html', title='Login', form=form
"""           

        


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = current_user

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))