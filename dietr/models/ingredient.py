from .. import database

class IngredientModel:
    '''Model for the ingredient pages. This model will handle all ineractions
    with the database.
    '''
    def add_ingredient(self, ingredient):
        # Get a cursor
        cursor = database.cursor()

        # Prepare query
        cursor.execute('''INSERT INTO ingredients (description, name)
                               VALUES (%s, %s)''')

        pass

    def edit_ingredient(self, ingredient):
        # Get a cursor
        cursor = database.cursor()

        # Prepare query
        cursor.execute('''UPDATE ingredients
                             SET description = %s,
                                 name        = %s
                           WHERE id          = %s''')

        pass

    def delete_ingredient(self, id):
        # Get a cursor
        cursor = database.cursor(MySQL.cursors.DictCursor)

        # Prepare query
        cursor.execute('''DELETE FROM allergen
                                WHERE ingredient_id = %s
                          DELETE FROM ingredient
                                WHERE id = %s
                          DELETE FROM recipes_ingredient
                                WHERE ingredient_id = %s'''

    def get_ingredient(self, id):
        # Get a cursor
        cursor = database.cursor()

        # Prepare query
        cursor.execute('''SELECT *
                            FROM ingredient
                           WHERE id = %s''', (id,))

        result = cursor.fetchone()

        ingredient = {
            'id': result[0],
            'name': result[1]
        }

        return ingredient

    def get_allergens(self, id):
        # Get a cursor
        cursor = database.cursor()

        # Prepare query
        cursor.execute('''SELECT category.id, category.name
                            FROM category
                                 INNER JOIN category_ingredient_relation
                                         ON category.id = category_ingredient_relation.id
                           WHERE ingredient_id = %s''', (id,))

        results = cursor.fetchall()

        allergens = []

        for result in results:
            allergens.append({
                'id': result[0],
                'name': result[1]
            })

        return allergens

    def get_ingredients(self):
        ingredients = []

        # Get a cursor
        cursor = database.cursor()

        # Prepare query
        cursor.execute('''SELECT *
                            FROM ingredient
                        ORDER BY name''')

        results = cursor.fetchall()

        for result in results:
            ingredients.append({
                'id': result[0],
                'name': result[1]
            })

        return ingredients
