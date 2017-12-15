from flask import render_template

from ..models.ingredient import Ingredient, IngredientModel

class IngredientController:
    def __init__(self):
        self.model = IngredientModel()

    def add(self):
        pass

    def edit(self, id):
        pass

    def delete(self, id):
        pass

    def view(self, id):
        # Get the ingredient from the database
        ingredient = self.model.get_ingredient(id)

        # Return the template
        return render_template('ingredient/view.html', ingredient = ingredient)
