from flask import abort, session
from flask_restful import Resource

from dietr import database
from dietr.views.api import api

prefix = '/roommates/<int:handle>'


class RoommatesAllergies(Resource):
    def delete(self, handle, id):
        # @TODO Fix bug with sessions not beign shared across domain
        '''
        if 'user' not in session:
            abort(403)

        user_id = session['user']
        '''
        user_id = 1

        query = '''DELETE roommates_allergies
                     FROM roommates_allergies
                          INNER JOIN allergies
                             ON allergies.id = roommates_allergies.allergy_id
                          INNER JOIN roommates
                             ON roommates.id = roommates_allergies.roommate_id
                    WHERE allergies.id = %s
                      AND roommates.handle = %s
                      AND roommates.user_id = %s'''

        database.commit(query, (id, handle, user_id))

    def post(self, handle, id, flag=0):
        # @TODO Fix bug with sessions not beign shared across domain
        '''
        if 'user' not in session:
            abort(403)

        user_id = session['user']
        '''
        user_id = 1

        query = '''INSERT INTO roommates_allergies (roommate_id, allergy_id)
                   VALUES ((SELECT id
                              FROM roommates
                             WHERE handle = %s
                               AND user_id = %s), %s)'''

        database.commit(query, (handle, user_id, id))


api.add_resource(RoommatesAllergies, f'{prefix}/allergies/<int:id>')


class RoommatesPreferences(Resource):
    def delete(self, handle, id):
        # @TODO Fix bug with sessions not beign shared across domain
        '''
        if 'user' not in session:
            abort(403)

        user_id = session['user']
        '''
        user_id = 1

        query = '''DELETE rp
                     FROM roommates_preferences AS rp
                          INNER JOIN ingredients
                             ON ingredients.id = rp.ingredient_id
                          INNER JOIN roommates
                             ON roommates.id = rp.roommate_id
                    WHERE ingredients.id = %s
                      AND roommates.handle = %s
                      AND roommates.user_id = %s'''

        database.commit(query, (id, handle, user_id))

    def post(self, handle, id, flag=0):
        # @TODO Fix bug with sessions not beign shared across domain
        '''
        if 'user' not in session:
            abort(403)

        user_id = session['user']
        '''
        user_id = 1

        query = '''INSERT INTO roommates_preferences (roommate_id, ingredient_id)
                   VALUES ((SELECT id
                              FROM roommates
                             WHERE handle = %s
                               AND user_id = %s), %s)'''

        database.commit(query, (handle, user_id, id))


api.add_resource(RoommatesPreferences, f'{prefix}/preferences/<int:id>')
