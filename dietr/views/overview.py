from flask import Blueprint, render_template

blueprint = Blueprint('overview', __name__)


@blueprint.route('/')
@blueprint.route('/dashboard')
def dashboard():
    return render_template('overview/dashboard.html')


@blueprint.route('/about')
def about():
    return render_template('overview/about.html')


@blueprint.route('/contact')
def contact():
    return render_template('overview/contact.html')


@blueprint.route('/legal')
def legal():
    return render_template('overview/legal.html')


@blueprint.route('/search')
def search():
    pass
