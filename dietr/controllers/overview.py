from flask import render_template

from .. import app
from ..models.overview import OverviewModel

model = OverviewModel()

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/legal')
def legal():
    # Return the template
    return render_template('legal.html')
