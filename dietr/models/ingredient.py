class IngredientModel:
    '''
    The ingredient model. This class is used to communicate with the database to
    extract end update data using the CRUD principle. Data may be exchaned using
    a intermediate object.
    '''
    def add_ingredient(self, ingredient):
        # Unpack tuple with data
        (description, name, id) = ingredient

        # Prepare query
        query = f'INSERT INTO ingredients (description, name) \
                       VALUES ({description}, {name})'

        pass

    def edit_ingredient(self, ingredient):
        # Unpack tuple with data
        (description, name, id) = ingredient

        # Prepare query
        query = f'UPDATE ingredients                  \
                     SET description = {description}, \
                         name        = {name}         \
                   WHERE id          = {id}'

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
