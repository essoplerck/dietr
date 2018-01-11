from dataclasses import dataclass, field

from dietr import database


@dataclass
class Allergen:
    id: int
    name: str


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
        query = '''INSERT INTO ingredient (name)
                   VALUES (%s);'''

        # Execute query
        database.commit(query, name)

    def edit_ingredient(self, ingredient):
        '''Update an ingredient in the database. Ingredient id will be
        preserved.
        '''
        query = '''UPDATE ingredient
                      SET name = %s
                    WHERE id = %s;'''

        # Execute query
        database.commit(query, (name, id))

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
        database.commit(query, tuple([id]) * 4)

    def get_ingredient(self, id):
        '''Fetch an ingredient from the database.'''
        query = '''SELECT id, name
                     FROM ingredient
                    WHERE id = %s;'''

        (id, name) = database.fetch(query, id)

        return Ingredient(id, name)

    def get_allergens(self, id):
        '''Fetch a list of allergens for a ingredient.'''
        query = '''SELECT category.id, category.name
                     FROM category
                          INNER JOIN category_ingredient_relation
                          ON category.id = category_ingredient_relation.id
                   WHERE ingredient_id = %s;'''

        allergens = []

        for allergen in database.fetch_all(query, id):
            (id, name) = allergen

            allergens.append(Allergen(id, name))

        return allergens

    def get_ingredients(self):
        '''Fetch a list of all ingredients.'''
        query = '''SELECT *
                     FROM ingredient
                    ORDER BY name;'''

        ingredients = []

        for ingredient in database.fetch_all(query):
            (id, name) = ingredient

            ingredients.append(Ingredient(id, name))

        return ingredients
