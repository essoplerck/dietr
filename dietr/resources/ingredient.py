from flask_restful import Resource

from dietr import database
from dietr.views.api import api


prefix = '/ingredients'


class Ingredients(Resource):
    def get(self, id):
        query = '''SELECT name
                     FROM ingredients
                    WHERE id = %s'''

        name = database.fetch(query, id)[0]

        ingredient = {
            'id': id,
            'name': name,
            'allergens': []
        }

        query = '''SELECT allergies.id, allergies.name
                     FROM allergies
                          INNER JOIN allergies_ingredients
                          ON allergies.id = allergies_ingredients.allergy_id
                   WHERE ingredient_id = %s'''

        for (id, name) in database.fetch_all(query, id):
            allergen = {
                'id': id,
                'name': name
            }

            ingredient['allergens'].append(allergen)

        return ingredient


api.add_resource(Ingredients, f'{prefix}/<int:id>')


class IngredientsOverview(Resource):
    def get(self):
        query = '''SELECT id, name
                     FROM ingredients'''

        ingredients = []

        for (id, name) in database.fetch_all(query):
            ingredient = {
                'id': id,
                'name': name
            }

            ingredients.append(ingredient)

        return ingredients


api.add_resource(IngredientsOverview, f'{prefix}')


class IngredientsSearch(Resource):
    def get(self, search):
        query = '''SELECT id, name
                     FROM ingredients
                    WHERE name LIKE %s'''

        ingredients = []

        for (id, name) in database.fetch_all(query, f'%{search}%'):
            ingredient = {
                'id': id,
                'name': name
            }

            ingredients.append(ingredient)

        return ingredients


api.add_resource(IngredientsSearch, f'{prefix}/search/<string:search>')
