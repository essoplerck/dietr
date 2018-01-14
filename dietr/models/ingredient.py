from dataclasses import dataclass, field

from dietr.database import database
from dietr.models.allergy import Allergy


@dataclass
class Ingredient:
    id: int
    name: str
    allergens: list = field(default_factory=list, init=False)


class IngredientModel:
    '''Model for the ingredient pages. This model will handle all ineractions
    with the database.
    '''
    def add_ingredient(self, name):
        '''Insert an ingredient into the database.'''
        query = '''INSERT INTO ingredients (name)
                   VALUES (%s)'''

        # Execute query
        database.commit(query, name)

    def delete_ingredient(self, id):
        '''Delete an ingredient from the database. Will also remove related
        tables.
        '''
        query = '''DELETE FROM ingredients
                    WHERE id = %s'''

        # Execute query
        database.commit(query, id)

    def get_ingredient(self, id):
        '''Fetch an ingredient from the database.'''
        query = '''SELECT id, name
                     FROM ingredients
                    WHERE id = %s'''

        return Ingredient(**database.fetch(query, id))

    def get_allergens(self, id):
        '''Fetch a list of allergens for a ingredient.'''
        query = '''SELECT allergies.id, allergies.name
                     FROM allergies
                          INNER JOIN allergies_ingredients
                          ON allergies.id = allergies_ingredients.allergy_id
                   WHERE ingredient_id = %s'''

        allergens = database.fetch_all(query, id)

        return [Allergy(**allergen) for allergen in allergens]

    def get_ingredients(self):
        '''Fetch a list of all ingredients.'''
        query = '''SELECT id, name
                     FROM ingredients
                    ORDER BY name'''

        ingredients = database.fetch_all(query)

        return [Ingredient(**ingredient) for ingredient in ingredients]

    def set_ingredient(self, id, name):
        '''Update an ingredient in the database. Ingredient id will be
        preserved.
        '''
        query = '''UPDATE ingredients
                      SET name = %s
                    WHERE id = %s'''

        # Execute query
        database.commit(query, (name, id))
