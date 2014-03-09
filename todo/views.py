from flask import render_template, request, flash, redirect, url_for, session, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import Signup, UserLogin
from models import User
from todo import app, db, login_manager
from werkzeug.security import check_password_hash


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
    form = UserLogin()

    if request.method == 'POST' and form.validate_on_submit() == False or request.method == 'GET':
        return render_template('login.html', form=form, title='Login')

    if request.method == 'POST' and form.validate_on_submit():
    
        user_pw = form.password.data
        user_email = form.email.data
        check_email = User.query.filter_by(email=user_email).first()
        if check_email is None:
            try:
                # check_pw throws error when email is invalid
                check_pw = check_email.check_password(user_pw)
            except AttributeError:
                flash('Invalid email')
                return render_template('login.html', form=form, title='Login')

        if check_email is not None:
            check_pw = check_email.check_password(user_pw)
            if check_pw is False:
                flash('Invalid password')
                return render_template('login.html', form=form, title='Login')

        if check_email is not None:
            check_pw = check_email.check_password(user_pw)
            if check_pw is True:
                session['logged_in'] = True
                flash('Logged in!')
                # login_user(check_email)
                return redirect('/')

    return render_template('login.html', form=form, title='Login')

        
@app.route("/logout")
def logout():
    session.pop('logged_in', None)

    # gets rid of flashed message from prev session
    session.pop('_flashes', None)
    return redirect('/')
