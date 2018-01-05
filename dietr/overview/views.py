from flask import Blueprint, render_template

overview = Blueprint('overview', __name__, template_folder = 'templates')

@overview.route('/')
@overview.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@overview.route('/about')
def about():
    return render_template('about.html')

@overview.route('/contact')
def contact():
    return render_template('contact.html')

@overview.route('/legal')
def legal():
    # Return the template
    return render_template('legal.html')
