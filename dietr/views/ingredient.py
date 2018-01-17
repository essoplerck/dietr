from flask import Blueprint, render_template

from dietr.models.ingredient import IngredientModel

blueprint = Blueprint('ingredient', __name__)

model = IngredientModel()


@blueprint.route('/ingredient/add')
def add_ingredient():
    '''The add action allows users to add an ingredient.'''
    pass


@blueprint.route('/ingredient/<int:id>/edit')
@blueprint.route('/ingredient/<int:id>/<string:name>/edit')
def edit_ingredient(id, name=None):
    '''The edit action allows users to change an ingredient.'''
    pass


@blueprint.route('/ingredient/<int:id>/remove')
@blueprint.route('/ingredient/<int:id>/<string:name>/remove')
def remove_ingredient(id, name=None):
    '''The remove action allows users to remove an ingredient for the
    database.
    '''
    pass


@blueprint.route('/ingredient/<int:id>')
@blueprint.route('/ingredient/<int:id>/<string:name>')
def ingredient(id, name=None):
    '''The view action allows users to view an ingredient.'''
    ingredient = model.get_ingredient(id)

    ingredient.allergens = model.get_allergens(id)

    # Return the template
    return render_template('ingredient/view.html', ingredient=ingredient)

@blueprint.route('/ingredients')
def ingredients():
    pass
