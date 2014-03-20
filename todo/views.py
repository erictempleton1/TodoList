from flask import render_template, request, flash, redirect, url_for, session, g
from forms import Signup, UserLogin, TodoList, UpdateList
from models import User, UserTodo
from todo import app, db
import datetime
from werkzeug.security import check_password_hash

@app.before_request
def load_user():
    try:
        g.user = User.query.filter_by(email=session['user_email']).first()
    except Exception:
        g.user = None

@app.route('/')
def index():
    try:
        user_name = g.user.name
    except AttributeError: # error thrown when user is not logged in
        user_name = 'Guest'

    return render_template('base.html', user=user_name)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Signup()

    if 'logged_in' in session:
        flash('You are already signed up! Please log out to create a new account.')
        return redirect('/')

    if request.method == 'POST' and form.validate_on_submit() == False or request.method == 'GET':
        return render_template('signup.html', form=form)

    if request.method == 'POST' and form.validate_on_submit():

        if User.query.filter_by(email=form.email.data.lower()).first() is not None:
            flash('Email already in use.')
            return render_template('signup.html', form=form)

        else:
            newuser = User(form.name.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()
            flash('Account created! Please login.')
            return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLogin()

    if 'logged_in' in session:
        flash('You are already logged in! Please log out to sign in as another user.')
        return redirect('/')

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
                return render_template('login.html', form=form)

        if check_email is not None:
            check_pw = check_email.check_password(user_pw)
            if check_pw is False:
                flash('Invalid password')
                return render_template('login.html', form=form)

        if check_email is not None:
            check_pw = check_email.check_password(user_pw)
            if check_pw is True:
                session['logged_in'] = True
                session['user_email'] = form.email.data
                flash('Logged in!')
                return redirect(url_for('display_list'))

    return render_template('login.html', form=form, title='Login')

@app.route('/create', methods=['GET', 'POST'])
def create_list():
    form = TodoList()

    if 'logged_in' not in session:
        flash('Please login or register to create your list!')
        return redirect('/')

    if request.method == 'POST' and form.validate_on_submit() == False or request.method == 'GET':
        return render_template('create.html', form=form, user=g.user.name)

    if request.method == 'POST' and form.validate_on_submit() == True:
        user = User.query.filter_by(email=g.user.email).first()
        list_submit = UserTodo(todo_item=form.todo_item.data, item_due_date=form.due_date.data, 
                                todo_item_note=form.item_note.data, create_date=datetime.datetime.utcnow(), 
                                user=user)
        db.session.add(list_submit)
        db.session.commit()
        flash('Item added!')
        return redirect(url_for('display_list'))

@app.route('/list')
def display_list():
    
    if 'logged_in' not in session:
        flash('Please login or register to view your list!')
        return redirect('/')
    
    if 'logged_in' in session:
        user = User.query.filter_by(email=g.user.email).first()
        get_list = user.user_list.all() # queries user_list db relation
        return render_template('list.html', get_list=get_list, user=g.user.name)

@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
def update_list(item_id):
    form = UpdateList()

    if 'logged_in' not in session:
        flash('Please login to view this page!')
        return redirect('/')

    if request.method == 'POST' and form.validate_on_submit() == False or request.method == 'GET':
        todo_item = UserTodo.query.get(item_id)
        return render_template('update.html', form=form, user=g.user.name, todo_item=todo_item)

    if request.method == 'POST' and form.validate_on_submit() == True:
        todo_item = UserTodo.query.get(item_id)
        todo_item.todo_item = form.todo_item.data
        todo_item.item_due_date = form.due_date.data
        db.session.commit()
        flash('List updated!')
        return redirect(url_for('display_list'))
        
        
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_email', None)
    session.pop('_flashes', None) # gets rid of flashed message from prev session
    return redirect('/')
