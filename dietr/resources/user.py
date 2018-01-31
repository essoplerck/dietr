from flask import abort, session
from flask_restful import Resource

from dietr import database
from dietr.views.api import api

prefix = '/users'


class UsersAllergies(Resource):
    def delete(self, id):
        if 'user' not in session:
            abort(403)

        user_id = session['user']

        query = '''DELETE FROM users_allergies
                    WHERE user_id = %s
                      AND allergy_id = %s'''

        database.commit(query, (user_id, id))

    def post(self, id, flag=0):
        if 'user' not in session:
            abort(403)

        user_id = session['user']

        query = '''INSERT INTO users_allergies (user_id, allergy_id, flag)
                   VALUES (%s, %s, %s)'''

        database.commit(query, (user_id, id, flag))


api.add_resource(UsersAllergies, f'{prefix}/allergies/<int:id>')


class UsersPreferences(Resource):
    def delete(self, id):
        if 'user' not in session:
            abort(403)

        user_id = session['user']

        query = '''DELETE FROM users_preferences
                    WHERE user_id = %s
                      AND ingredient_id = %s'''

        database.commit(query, (user_id, id))

    def post(self, id, flag=0):
        if 'user' not in session:
            abort(403)

        user_id = session['user']

        query = '''INSERT INTO users_preferences (user_id, ingredient_id, flag)
                   VALUES (%s, %s, %s)'''

        database.commit(query, (user_id, id, flag))


api.add_resource(UsersPreferences, f'{prefix}/preferences/<int:id>')
