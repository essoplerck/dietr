from flask import Blueprint, render_template

from dietr.models import model

blueprint = Blueprint('allergy', __name__)


@blueprint.route('/allergy/add', methods=['GET', 'POST'])
def add():
    """Allow users to add an allergy to the database."""
    pass


@blueprint.route('/allergy/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """Allow user to edit the name of an allergy."""
    pass


@blueprint.route('/allergy/<int:id>/remove', methods=['GET', 'POST'])
def remove(id):
    """Allow users to remove an allergy from the database."""
    pass


@blueprint.route('/allergy/<int:id>')
def view(id):
    """Allow users to view an allergy."""
    allergy = model.allergy.get_allergy(id)

    return render_template('allergy/view.jinja', allergy=allergy)


@blueprint.route('/allergies')
def overview():
    """Allow users to view all allergies."""
    pass
