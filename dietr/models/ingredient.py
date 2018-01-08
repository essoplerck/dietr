from .. import connection


class IngredientModel:
    '''Model for the ingredient pages. This model will handle all ineractions
    with the database.
    '''
    def add_ingredient(self, ingredient):
        '''Insert an ingredient into the database.'''
        query = '''INSERT INTO ingredient (description, name)
                        VALUES (%s, %s)'''

        cursor = connection.cursor()
        cursor.execute(query, (ingredient['name'], ingredient['id']))

        # Execute query
        return connection.commit()

    def edit_ingredient(self, ingredient):
        '''Update an ingredient in the database. Ingredient id will be
        preserved.
        '''
        query = '''UPDATE ingredient
                      SET name = %s
                    WHERE id   = %s'''

        cursor = connection.cursor()
        cursor.execute(query, (ingredient['name'], ingredient['id']))

        # Execute query
        return connection.commit()

    def remove_ingredient(self, id):
        '''Delete an ingredient from the database. Will also remove related
        tables.
        '''
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM ingredient
                           WHERE id = %s''', id)

        cursor.execute('''DELETE FROM allergen
                           WHERE ingredient_id = %s''', id)

        cursor.execute('''DELETE FROM recipes_ingredient
                           WHERE ingredient_id = %s''', id)

        cursor.execute('''DELETE FROM person_ingredient_relation
                           WHERE ingredient_id = %s''', id)

        # Execute queries
        return connection.commit()

    def get_ingredient(self, id):
        '''Fetch an ingredient from the database.'''
        query = '''SELECT *
                     FROM ingredient
                    WHERE id = %s'''

        cursor = connection.cursor()
        cursor.execute(query, id)

        # Return ingredient
        return cursor.fetchone()

    def get_allergens(self, id):
        '''Fetch a list of allergens for a ingredient.'''
        query = '''SELECT category.id, category.name
                     FROM category
                          INNER JOIN category_ingredient_relation
                                  ON category.id = category_ingredient_relation.id
                   WHERE ingredient_id = %s'''

        cursor = connection.cursor()
        cursor.execute(query, id)

        # Return allergens
        return cursor.fetchall()

    def get_ingredients(self):
        '''Fetch a list of all ingredients.'''
        query = '''SELECT *
                     FROM ingredient
                 ORDER BY name'''

        cursor = connection.cursor()
        cursor.execute(query)

        # Return ingredients
        return cursor.fetchall()
