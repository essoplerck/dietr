from .. import connection

class IngredientModel:
    '''Model for the ingredient pages. This model will handle all ineractions
    with the database.
    '''
    def add_ingredient(self, ingredient):
        query = '''INSERT INTO ingredients (description, name)
                        VALUES (%s, %s)'''

        cursor = connection.cursor()
        cursor.execute(query, None)

        # Execute query
        connection.commit()

    def edit_ingredient(self, ingredient):
        query = '''UPDATE ingredients
                      SET description = %s,
                          name        = %s
                    WHERE id          = %s'''

        cursor = connection.cursor()
        cursor.execute(query, None)

        # Execute query
        connection.commit()

    def delete_ingredient(self, id):
        query = '''DELETE FROM allergen
                         WHERE ingredient_id = %s
                   DELETE FROM ingredient
                         WHERE id = %s
                   DELETE FROM recipes_ingredient
                         WHERE ingredient_id = %s'''

        cursor = connection.cursor()
        cursor.execute(query, (id, id, id))

        # Execute query
        connection.commit()

    def get_ingredient(self, id):
        query = '''SELECT *
                     FROM ingredient
                    WHERE id = %s'''

        cursor = connection.cursor()
        cursor.execute(query, id)

        ingredient = cursor.fetchone()

        return ingredient

    def get_allergens(self, id):
        query = '''SELECT category.id, category.name
                     FROM category
                          INNER JOIN category_ingredient_relation
                                  ON category.id = category_ingredient_relation.id
                   WHERE ingredient_id = %s'''

        cursor = connection.cursor()
        cursor.execute(query, id)

        allergens = cursor.fetchall()

        return allergens

    def get_ingredients(self):
        query = '''SELECT *
                     FROM ingredient
                 ORDER BY name'''

        cursor = connection.cursor()
        cursor.execute(query)

        ingredients = cursor.fetchall()

        return ingredients
