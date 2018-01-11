from dietr import database


class IngredientModel:
    '''Model for the ingredient pages. This model will handle all ineractions
    with the database.
    '''
    def add_ingredient(self, ingredient):
        '''Insert an ingredient into the database.'''
        query = '''INSERT INTO ingredient (name)
                   VALUES (%s);'''

        # Execute query
        database.commit(query, (ingredient['name']))

    def edit_ingredient(self, ingredient):
        '''Update an ingredient in the database. Ingredient id will be
        preserved.
        '''
        query = '''UPDATE ingredient
                      SET name = %s
                    WHERE id = %s;'''

        # Execute query
        database.commit(query, (ingredient['name'], ingredient['id']))

    def remove_ingredient(self, id):
        '''Delete an ingredient from the database. Will also remove related
        tables.
        '''
        query = '''DELETE FROM ingredient
                    WHERE id = %s;
                   DELETE FROM category_ingredient_relation
                    WHERE ingredient_id = %s;
                   DELETE FROM recipe_ingredient_relation
                    WHERE ingredient_id = %s;
                   DELETE FROM person_ingredient_relation
                    WHERE ingredient_id = %s;'''

        # Execute query
        database.commit(query, (id, id, id, id))

    def get_ingredient(self, id):
        '''Fetch an ingredient from the database.'''
        query = '''SELECT *
                     FROM ingredient
                    WHERE id = %s;'''

        # Return ingredient
        return database.fetch(query, id)

    def get_allergens(self, id):
        '''Fetch a list of allergens for a ingredient.'''
        query = '''SELECT category.id, category.name
                     FROM category
                          INNER JOIN category_ingredient_relation
                          ON category.id = category_ingredient_relation.id
                   WHERE ingredient_id = %s;'''

        # Return allergens
        return database.fetch_all(query, id)

    def get_ingredients(self):
        '''Fetch a list of all ingredients.'''
        query = '''SELECT *
                     FROM ingredient
                    ORDER BY name;'''

        # Return ingredients
        return database.fetch_all(query)
