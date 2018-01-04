from flask import render_template

from .. import app
from ..models.ingredient import IngredientModel

model = IngredientModel()

@app.route('/ingredient/add')
def add_ingredient():
    '''The add action allows users to add an ingredient.'''
    pass

@app.route('/ingredient/<int:id>/edit')
@app.route('/ingredient/<int:id>/<string:name>/edit')
def edit_ingredient(id, name = None):
    '''The edit action allows users to change an ingredient.'''
    pass

@app.route('/ingredient/<int:id>/remove')
@app.route('/ingredient/<int:id>/<string:name>/remove')
def remove_ingredient(id, name = None):
    '''The remove action allows users to remove an ingredient for the
    database.
    '''
    pass

@app.route('/ingredient/<int:id>')
@app.route('/ingredient/<int:id>/<string:name>')
def view_ingredient(id, name = None):
    '''The view action allows users to view an ingredient.'''
    ingredient = model.get_ingredient(id)

    ingredient['allergens'] = model.get_allergens(id)

    # Return the template
    return render_template('ingredient/view.html', ingredient = ingredient)
