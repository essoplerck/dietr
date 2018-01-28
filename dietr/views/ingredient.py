from flask import Blueprint, render_template

from dietr.models import model

blueprint = Blueprint('ingredient', __name__)


@blueprint.route('/ingredient/add', methods=['GET', 'POST'])
def add():
    pass


@blueprint.route('/ingredient/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    pass


@blueprint.route('/ingredient/<int:id>/remove', methods=['GET', 'POST'])
def remove(id):
    pass


@blueprint.route('/ingredient/<int:id>')
def view(id):
    ingredient = model.ingredient.get_ingredient(id)

    ingredient.allergens = model.ingredient.get_allergens(id)

    return render_template('ingredient/view.jinja', ingredient=ingredient)


@blueprint.route('/ingredients')
def overview():
    pass
