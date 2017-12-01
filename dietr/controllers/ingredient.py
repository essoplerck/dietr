from flask import render_template

from dietr.models.ingredient import IngredientModel

class IngredientController:
    def add(self):
        pass

    def delete(self, id):
        pass

    def edit(self, id):
        pass

    def view(self, id):
        # Get the ingredient from the database
        ingredient = self.model.get_ingredient(id)

        # Return the template
        return render_template('ingredient/view.html', ingredient = ingredient)

    def __init__(self):
        self.model = IngredientModel()
