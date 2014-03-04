from flask import render_template, request, flash, redirect, url_for, session, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import Signup, UserLogin
from models import User
from todo import app, db, login_manager
from werkzeug.security import check_password_hash

user_pw = 'eric'
user_email = User.query.filter_by(email='eric1@eric.com').first()

# multiple if's used to check all conditions
# elif stops if one of the conditions is met
if user_email is None:
    try:
        # check_pw throws error when email is invalid
        check_pw = user_email.check_password(user_pw)
    except AttributeError:
        print 'Invalid email'

if user_email is not None:
    check_pw = user_email.check_password(user_pw)
    if check_pw is False:
        print 'Invalid password'

if user_email is not None:
    check_pw = user_email.check_password(user_pw)
    if check_pw is True:
        print 'Logged in!'

        