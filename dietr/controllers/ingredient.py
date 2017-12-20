from flask import render_template

from .. import app
from ..models.ingredient import Ingredient, IngredientModel

class IngredientController:
    '''Controller for the ingredient pages. This controller will contain
    actions for all routes.
    '''
    def __init__(self):
        # Get the model for the ingredient pages
        self.model = IngredientModel()

    def add(self):
        '''The add action allows users to add an ingredient to the database.'''
        pass

    def edit(self, id):
        '''The edit action allows users to change an ingredient.'''
        pass

    def delete(self, id):
        '''The delete action allows users to remove an ingredient for the
        database.
        '''
        pass

    def view(self, id):
        '''The view action allows users to view an ingredient.'''
        # Get the ingredient from the database
        ingredient = self.model.get_ingredient(id)

        # Return the template
        return render_template('ingredient/view.html', ingredient = ingredient)

controller = IngredientController()

@app.route('/ingredient/<int:id>')
@app.route('/ingredient/<int:id>/<string:name>')
def ingredient(id, name = None):
    return controller.view(id)

@app.route('/ingredient/add')
def ingredient_add():
    return controller.add()

@app.route('/ingredient/<int:id>/edit')
@app.route('/ingredient/<int:id>/<string:name>/edit')
def ingredient_edit(id, name = None):
    return controller.edit(id)

@app.route('/ingredient/<int:id>/delete')
@app.route('/ingredient/<int:id>/<string:name>/delete')
def ingredient_delete(id, name = None):
    return controller.delete(id)
