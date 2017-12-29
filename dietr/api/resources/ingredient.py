from flask_restful import Resource

from .. import api, connection

class Ingredients(Resource):
    def get(self, id):
        cursor = connection.cursor()
        cursor.execute('''SELECT *
                            FROM ingredient
                           WHERE id = %s''', id)

        ingredient = cursor.fetchone()

        return ingredient

api.add_resource(Ingredients, '/ingredients/<int:id>')
