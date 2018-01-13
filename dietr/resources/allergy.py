from flask_restful import Resource

from dietr import database
from dietr.views.api import api


prefix = '/allergies'


class Allergies(Resource):
    def get(self, id):
        query = '''SELECT id, name
                     FROM allergies
                    WHERE id = %s'''

        return database.fetch(query, id)


api.add_resource(Allergies, f'{prefix}/<int:id>')


class AllergiesOverview(Resource):
    def get(self):
        query = '''SELECT id, name
                     FROM allergies'''

        return database.fetch_all(query)


api.add_resource(AllergiesOverview, prefix)


class AllergiesSearch(Resource):
    def get(self, search):
        query = '''SELECT id, name
                     FROM allergies
                    WHERE name LIKE %s'''

        return database.fetch_all(query, f'%{search}%')


api.add_resource(AllergiesSearch, f'{prefix}/search/<string:search>')
