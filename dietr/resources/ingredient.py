from flask_restful import Resource

from dietr import database
from dietr.views.api import api


prefix = '/ingredients'


class Ingredients(Resource):
    def get(self, id):
        query = '''SELECT id, name
                     FROM ingredients
                    WHERE id = %s'''

        ingredient = database.fetch(query, id)

        query = '''SELECT allergies.id, allergies.name
                     FROM allergies
                          INNER JOIN allergies_ingredients
                          ON allergies.id = allergies_ingredients.allergy_id
                   WHERE ingredient_id = %s'''

        ingredient['allergens'] = database.fetch_all(query, id)

        return ingredient


api.add_resource(Ingredients, f'{prefix}/<int:id>')


class IngredientsOverview(Resource):
    def get(self):
        query = '''SELECT id, name
                     FROM ingredients'''

        return database.fetch_all(query)


api.add_resource(IngredientsOverview, f'{prefix}')


class IngredientsSearch(Resource):
    def get(self, search):
        query = '''SELECT id, name
                     FROM ingredients
                    WHERE name LIKE %s'''

        return database.fetch_all(query, f'%{search}%')


api.add_resource(IngredientsSearch, f'{prefix}/search/<string:search>')
