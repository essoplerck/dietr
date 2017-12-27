from .. import database

class IngredientModel:
    '''Model for the ingredient pages. This model will handle all ineractions
    with the database.
    '''
    def add_ingredient(self, ingredient):
        # Prepare query
        query = f'INSERT INTO ingredients (description, name) \
                       VALUES ({ingredient.description}, {ingredient.name})'

        pass

    def edit_ingredient(self, ingredient):
        # Prepare query
        query = f'UPDATE ingredients                             \
                     SET description = {ingredient.description}, \
                         name        = {ingredient.name}         \
                   WHERE id          = {ingredient.id}'

        pass

    def delete_ingredient(self, id):
        # Prepare query
        query = f'DELETE FROM allergen             \
                        WHERE ingredient_id = {id} \
                  DELETE FROM ingredient           \
                        WHERE id = {id}            \
                  DELETE FROM recipes_ingredient   \
                        WHERE ingredient_id = {id}'

        pass

    def get_ingredient(self, id):
        # Prepare query
        query = f'SELECT *          \
                    FROM ingredient \
                   WHERE id = {id}'

        return ingredient

    def get_ingredients(self):
        # Prepare query
        query = f'SELECT *          \
                    FROM ingredient \
                ORDER BY name'

        return ingredients
