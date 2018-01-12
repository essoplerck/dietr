from dataclasses import dataclass, field

from flask_restful import Resource

from dietr import database
from dietr.api import api

@dataclass
class Ingredient:
    id: int
    name: str
    allergens: list = field(default_factory=list, init=False)


class Ingredients(Resource):
    def get(self, id):
        query = '''SELECT name
                     FROM ingredients
                    WHERE id = %s'''

        name = database.fetch(query, id)[0]

        ingredient = Ingredient(id, name)

        query = '''SELECT allergies.id, allergies.name
                     FROM allergies
                          INNER JOIN allergies_ingredients
                          ON allergies.id = allergies_ingredients.allergy_id
                   WHERE ingredient_id = %s'''

        for (id, name) in database.fetch_all(query, id):
            ingredient.allergens.append(Allergen(id, name))

        return ingredient


api.add_resource(Ingredients, '/ingredients/<int:id>')


class IngredientsOverview(Resource):
    def get(self):
        query = '''SELECT id, name
                     FROM ingredients'''

        ingredients = []

        for (id, name) in database.fetch_all(query):
            ingredients.append(Ingredient(id, name))

        return ingredients


api.add_resource(IngredientsOverview, '/ingredients')


class IngredientsSearch(Resource):
    def get(self, search):
        query = '''SELECT id, name
                     FROM ingredients
                    WHERE name LIKE %s'''

        ingredients = []

        for (id, name) in database.fetch_all(query, f'%{search}%'):
            ingredients.append(Ingredient(id, name))

        return ingredients


api.add_resource(IngredientsSearch, '/ingredients/search/<string:search>')
