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

    if form.validate_on_submit():
        session['remember_me'] = True
        user_email = User.query.filter_by(email=form.email.data).first()
        user_pw = user_email.check_password(form.password.data)
        reg_user = User.query.filter_by(email=form.email.data, pw_hash=user_pw).first()
        login_user(reg_user)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form, title='Login')

        
            
        
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))