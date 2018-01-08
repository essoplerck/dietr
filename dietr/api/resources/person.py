from flask import session
from flask_restful import Resource, fields, marshal_with

from .. import api, connection


prefix = '/persons/<int:handle>'

resource_fields = {
    'flag': fields.Int
}


class PersonsAllergies(Resource):
    def delete(self, handle, id):
        user = 1

        query = '''DELETE pc
                     FROM person_category_relation AS pc
                          INNER JOIN category
                             ON category.id = pc.category_id
                          INNER JOIN person
                             ON person.id   = pc.person_id
                    WHERE category.id       = %s
                      AND person.account_id = %s
                      AND person.handle     = %s'''

        cursor = connection.cursor()
        status = cursor.execute(query, (id, user, handle))

        connection.commit()

        return status

    def post(self, handle, id, flag=0):
        user = 1

        query = '''INSERT INTO person_category_relation (person_id, category_id, flag)
                   SELECT (
                          SELECT person.id
                            FROM person
                           WHERE person.account_id = %
                             AND person.handle     = %s), (%s), (0)'''

        query = '''INSERT INTO person_category_relation (person_id, category_id, flag)
                   SELECT person.id, %s, 0
                     FROM person_category_relation AS pc
                          INNER JOIN person
                             ON person.id   = pc.person_id
                    WHERE person.account_id = %s
                      AND person.handle     = %s'''

        cursor = connection.cursor()
        status = cursor.execute(query, (id, user, handle))

        connection.commit()

        return status


api.add_resource(PersonsAllergies, f'{prefix}/allergies/<int:id>')


class PersonsIngredients(Resource):
    def delete(self, handle, id):
        user = 1

        query = '''DELETE pi
                     FROM person_ingredient_relation AS pi
                          INNER JOIN ingredient
                             ON ingredient.id = pi.ingredient_id
                          INNER JOIN person
                             ON person.id     = pi.person_id
                    WHERE ingredient.id       = %s
                      AND person.account_id   = %s
                      AND person.handle       = %s'''

        cursor = connection.cursor()
        status = cursor.execute(query, (id, user, handle))

        connection.commit()

        return status

    def post(self, handle, id, flag=0):
        user = 1

        query = '''INSERT INTO person_ingredient_relation (person_id, ingredient_id, flag)
                   SELECT (
                          SELECT person.id
                            FROM person
                           WHERE person.account_id = %
                             AND person.handle     = %s), (%s), (0)'''

        query = '''INSERT INTO person_ingredient_relation (person_id, ingredient_id, flag)
                   SELECT person.id, %s, 0
                     FROM person_category_relation AS pc
                          INNER JOIN person
                             ON person.id   = pc.person_id
                    WHERE person.account_id = %s
                      AND person.handle     = %s'''

        cursor = connection.cursor()
        status = cursor.execute(query, (id, user, handle))

        connection.commit()

        return status


api.add_resource(PersonsIngredients, f'{prefix}/ingredients/<int:id>')
