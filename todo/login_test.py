from flask import render_template, request, flash, redirect, url_for, session, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import Signup, UserLogin
from models import User
from todo import app, db, login_manager
from werkzeug.security import check_password_hash

user_pw = 'eric'
user_email = 'eric@eric.com'
check_email = User.query.filter_by(email=user_email).first()


def user_login():
    """ multiple if's used to check all conditions
        elif stops if one of the conditions is met """

    if check_email is None:
        try:
            # check_pw throws error when email is invalid
            check_pw = check_email.check_password(user_pw)
        except AttributeError:
            return 'Invalid email'

    if check_email is not None:
        check_pw = check_email.check_password(user_pw)
        if check_pw is False:
            return 'Invalid password'

    if check_email is not None:
        check_pw = check_email.check_password(user_pw)
        if check_pw is True:
            return 'Logged in!'

print user_login()

        