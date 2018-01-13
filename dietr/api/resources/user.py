from flask import abort, session
from flask_restful import Resource

from dietr import database
from dietr.api import api


prefix = '/users'


class UsersAllergies(Resource):
    def delete(self, handle, id):
        if 'user' not in session:
            abort(403)

        user_id = session['user']

        query = '''DELETE FROM users_allergies
                    WHERE user_id = %s
                      AND allergy_id = %s'''

        database.commit(query, (user_id, id))

    def post(self, handle, id, flag=0):
        if 'user' not in session:
            abort(403)

        user_id = session['user']

        query = '''INSERT INTO users_allergies (id, allergy_id, flag)
                   SELECT %s, %s, %s'''

        database.commit(query, (user_id, id, flag))


api.add_resource(UsersAllergies, f'{prefix}/allergies/<int:id>')


class UsersPreferences(Resource):
    def delete(self, handle, id):
        if 'user' not in session:
            abort(403)

        user_id = session['user']

        query = '''DELETE FROM users_preferences
                    WHERE user_id = %s
                      AND ingredient_id = %s'''

        database.commit(query, (user_id, id))

    def post(self, handle, id, flag=0):
        if 'user' not in session:
            abort(403)

        user_id = session['user']

        query = '''INSERT INTO users_preferences (id, ingredient_id, flag)
                   SELECT %s, %s, %s'''

        database.commit(query, (user_id, id, flag))


api.add_resource(UsersPreferences, f'{prefix}/preferences/<int:id>')
