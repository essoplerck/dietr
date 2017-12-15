class Ingredient:
    def __init__(self, id, description, name):
        self.id          = id
        self.description = description
        self.name        = name

class IngredientModel:
    '''
    The ingredient model. This class is used to communicate with the database to
    extract end update data using the CRUD principle. Data may be exchaned using
    a intermediate object.
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
