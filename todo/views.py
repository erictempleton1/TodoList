from flask import render_template
from todo import app

@app.route('/')
def index():
    return render_template('base.html', title='Home')