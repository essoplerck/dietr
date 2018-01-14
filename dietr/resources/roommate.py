from flask import abort, session
from flask_restful import Resource

from dietr import database
from dietr.views.api import api


prefix = '/roommmates/<int:handle>'


class RoommmatesAllergies(Resource):
    def delete(self, handle, id):
        if 'user' not in session:
            abort(403)

        user_id = session['user']

        query = '''DELETE roommates_allergies
                     FROM roommates_allergies
                          INNER JOIN allergies
                             ON allergens.id = roommates_allergies.allergy_id
                          INNER JOIN roommates
                             ON roommates.id = roommates_allergies.roommate_id
                    WHERE allergies.id = %s
                      AND roommates.handle = %s
                      AND roommates.user_id = %s'''

        database.commit(query, (id, handle, user_id))

    def post(self, handle, id, flag=0):
        if 'user' not in session:
            abort(403)

        user_id = session['user']

        query = '''INSERT INTO ra (roommate_id, allergy_id, flag)
                   SELECT roommates.id, %s, %s
                     FROM roommates_allergies AS ra
                          INNER JOIN roommates
                             ON roommates.id = ra.roommates_id
                    WHERE roommates.handle = %s
                      AND roommates.user_id = %s'''

        database.commit(query, (id, flag, handle, user_id))


api.add_resource(RoommmatesAllergies, f'{prefix}/allergies/<int:id>')


class RoommmatesPreferences(Resource):
    def delete(self, handle, id):
        if 'user' not in session:
            abort(403)

        user_id = session['user']

        query = '''DELETE rp
                     FROM roommates_preferences AS rp
                          INNER JOIN ingredients
                             ON preferences.id = rp.ingredient_id
                          INNER JOIN roommates
                             ON roommates.id = rp.roommate_id
                    WHERE ingredients.id = %s
                      AND roommates.handle = %s
                      AND roommates.user_id = %s'''

        database.commit(query, (id, handle, user_id))

    def post(self, handle, id, flag=0):
        if 'user' not in session:
            abort(403)

        user_id = session['user']

        query = '''INSERT INTO rp (roommate_id, ingredient_id, flag)
                   SELECT roommates.id, %s, %s
                     FROM roommates_preferences AS rp
                          INNER JOIN roommates
                             ON roommates.id = rp.roommates_id
                    WHERE roommates.handle = %s
                      AND roommates.user_id = %s'''

        database.commit(query, (id, flag, handle, user_id))


api.add_resource(RoommmatesPreferences, f'{prefix}/preferences/<int:id>')