from flask import Blueprint, render_template

blueprint = Blueprint('overview', __name__)


@blueprint.route('/')
@blueprint.route('/dashboard')
def dashboard():
    return render_template('overview/dashboard.jinja')


@blueprint.route('/about')
def about():
    return render_template('overview/about.jinja')
