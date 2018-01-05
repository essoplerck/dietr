from flask import Blueprint, render_template

blueprint = Blueprint('overview', __name__)

@blueprint.route('/')
@blueprint.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@blueprint.route('/about')
def about():
    return render_template('about.html')

@blueprint.route('/contact')
def contact():
    return render_template('contact.html')

@blueprint.route('/legal')
def legal():
    # Return the template
    return render_template('legal.html')
