from flask import Blueprint, render_template

ingredient = Blueprint('ingredient', __name__, template_folder = 'templates')

from .model import IngredientModel

model = IngredientModel()

@ingredient.route('/ingredient/add')
def add_ingredient():
    '''The add action allows users to add an ingredient.'''
    pass

@ingredient.route('/ingredient/<int:id>/edit')
@ingredient.route('/ingredient/<int:id>/<string:name>/edit')
def edit_ingredient(id, name = None):
    '''The edit action allows users to change an ingredient.'''
    pass

@ingredient.route('/ingredient/<int:id>/remove')
@ingredient.route('/ingredient/<int:id>/<string:name>/remove')
def remove_ingredient(id, name = None):
    '''The remove action allows users to remove an ingredient for the
    database.
    '''
    pass

@ingredient.route('/ingredient/<int:id>')
@ingredient.route('/ingredient/<int:id>/<string:name>')
def view_ingredient(id, name = None):
    '''The view action allows users to view an ingredient.'''
    ingredient = model.get_ingredient(id)

    ingredient['allergens'] = model.get_allergens(id)

    # Return the template
    return render_template('view.html', ingredient = ingredient)
