from dataclasses import dataclass, field

from flask_restful import Resource

from dietr import database
from dietr.api import api


prefix = '/allergies'


class Allergies(Resource):
    def get(self, id):
        query = '''SELECT name
                     FROM allergies
                    WHERE id = %s'''

        name = database.fetch(query, id)[0]

        allergy = {
            'id': id,
            'name': name
        }

        return allergy


api.add_resource(Allergies, f'{prefix}/<int:id>')


class AllergiesOverview(Resource):
    def get(self):
        query = '''SELECT id, name
                     FROM allergies'''

        allergies = []

        for (id, name) in database.fetch_all(query):
            allergy = {
                'id': id,
                'name': name
            }

            allergies.append(allergy)

        return allergies


api.add_resource(AllergiesOverview, prefix)


class AllergiesSearch(Resource):
    def get(self, search):
        query = '''SELECT id, name
                     FROM allergies
                    WHERE name LIKE %s'''

        allergies = []

        for (id, name) in database.fetch_all(query, f'%{search}%'):
            allergy = {
                'id': id,
                'name': name
            }

            allergies.append(allergy)

        return allergies


api.add_resource(AllergiesSearch, f'{prefix}/search/<string:search>')
