from flask_restful import Resource

from dietr.api import api, connection


class Ingredients(Resource):
    def get(self, id):
        cursor = connection.cursor()
        cursor.execute('''SELECT *
                            FROM ingredient
                           WHERE id = %s''', id)

        ingredient = cursor.fetchone()

        cursor.execute('''SELECT category.id, category.name
                            FROM category
                                 INNER JOIN category_ingredient_relation AS ci
                                    ON category.id = ci.id
                           WHERE ingredient_id = %s''', id)

        ingredient['allergies'] = cursor.fetchall()

        return ingredient


api.add_resource(Ingredients, '/ingredients/<int:id>')


class IngredientsOverview(Resource):
    def get(self):
        cursor = connection.cursor()
        cursor.execute('''SELECT *
                            FROM ingredient''')

        ingredients = cursor.fetchall()

        return ingredients


api.add_resource(IngredientsOverview, '/ingredients')


class IngredientsSearch(Resource):
    def get(self, query):
        cursor = connection.cursor()
        cursor.execute('''SELECT *
                            FROM ingredient
                           WHERE name LIKE %s''', f'%{query}%')

        ingredients = cursor.fetchall()

        return ingredients


api.add_resource(IngredientsSearch, '/ingredients/search/<string:query>')
