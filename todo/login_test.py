from flask import render_template, request, flash, redirect, url_for, session, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import Signup, UserLogin
from models import User
from todo import app, db, login_manager
from werkzeug.security import check_password_hash


user_email = User.query.filter_by(email='jojo@jojo.com').first()
check_pw = user_email.check_password('jojo')


