from flask import render_template

from .. import app
from ..models.ingredient import IngredientModel

model = IngredientModel()

@app.route('/ingredient/<int:id>')
@app.route('/ingredient/<int:id>/<string:name>')
def view_ingredient(id, name = None):
    '''The view action allows users to view an ingredient.'''
    # Get the ingredient from the database
    ingredient = model.get_ingredient(id)

    allergens = model.get_allergens(ingredient['id'])

    # Return the template
    return render_template('ingredient/view.html', ingredient = ingredient)

@app.route('/ingredient/add')
def add_ingredient():
    '''The add action allows users to add an ingredient to the database.'''

    pass

@app.route('/ingredient/<int:id>/edit')
@app.route('/ingredient/<int:id>/<string:name>/edit')
def edit_ingredient(id, name = None):
    '''The edit action allows users to change an ingredient.'''

    pass

@app.route('/ingredient/<int:id>/delete')
@app.route('/ingredient/<int:id>/<string:name>/delete')
def delete_ingredient(id, name = None):
    '''The delete action allows users to remove an ingredient for the
    database.
    '''

    pass
