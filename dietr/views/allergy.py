from flask import Blueprint, render_template

from dietr.models.allergy import AllergyModel

blueprint = Blueprint('allergy', __name__)

model = AllergyModel()


@blueprint.route('/allergy/add', methods=['GET', 'POST'])
def add():
    pass


@blueprint.route('/allergy/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    pass


@blueprint.route('/allergy/<int:id>/remove', methods=['GET', 'POST'])
def remove(id):
    pass


@blueprint.route('/allergy/<int:id>')
def view(id):
    allergy = model.get_allergy(id)

    return render_template('allergy/view.jinja', allergy=allergy)


@blueprint.route('/allergies')
def overview():
    pass
