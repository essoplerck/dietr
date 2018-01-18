from flask import Blueprint, render_template

from dietr.models.ingredient import IngredientModel

blueprint = Blueprint('ingredient', __name__)

model = IngredientModel()


@blueprint.route('/ingredient/add', methods=['GET', 'POST'])
def add():
    '''The add action allows users to add an ingredient.'''
    pass


@blueprint.route('/ingredient/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    '''The edit action allows users to change an ingredient.'''
    pass


@blueprint.route('/ingredient/<int:id>/remove', methods=['GET', 'POST'])
def remove(id):
    '''The remove action allows users to remove an ingredient for the
    database.
    '''
    pass


@blueprint.route('/ingredient/<int:id>')
def view(id):
    '''The view action allows users to view an ingredient.'''
    ingredient = model.get_ingredient(id)

    ingredient.allergens = model.get_allergens(id)

    # Return the template
    return render_template('ingredient/view.html', ingredient=ingredient)


@blueprint.route('/ingredients')
def overview():
    pass
