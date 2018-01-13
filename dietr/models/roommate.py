from dataclasses import dataclass, field

from flask import session

from dietr import database
from dietr.models.allergy import Allergy
from dietr.models.ingredient import Ingredient


@dataclass
class Roommate:
    id: int
    handle: int
    user_id: int
    first_name: str
    middle_name: str
    last_name: str
    allergies: list = field(default_factory=list, init=False)
    preferences: list = field(default_factory=list, init=False)

    @property
    def name(self):
        if self.middle_name:
            return f'{self.first_name} {self.middle_name} {self.last_name}'

        else:
            return f'{self.first_name} {self.last_name}'


class RoommateModel:
    '''Model for the person pages. This model will handle all ineractions
    with the database.
    '''
    def add_person(self, handle, first_name, middle_name, last_name):
        '''Insert a person into the database.'''
        user_id = session['user']

        query = '''INSERT INTO roommates (handle, user_id, first_name, middle_name, last_name)
                   VALUES (%s, %s, %s, %s, %s)'''

        database.commit(query, (handle, user_id, first_name, middle_name, last_name))

    def set_roommate(self, handle, first_name, middle_name, last_name):
        '''Update a person in the database. Person id will be preserved.'''
        user_id = session['user']

        query = '''UPDATE roommates
                      SET first_name = %s,
                          middle_name = %s,
                          last_name = %s
                    WHERE handle = %s
                      AND user_id = %s'''

        database.commit(query, (first_name, middle_name, last_name, id, user_id))

    def delete_roommate(self, handle):
        '''Delete a person from the database. Will also remove related
        tables.
        '''
        user_id = session['user']

        query = '''DELETE FROM roommates
                    WHERE handle = %s
                      AND user_id = %s'''

        # Execute query
        database.commit(query, (handle, user_id))

    def get_roommate(self, handle):
        '''Fetch a person from the database.'''
        user_id = session['user']

        query = '''SELECT id, first_name, middle_name, last_name
                     FROM roommates
                    WHERE handle = %s
                      AND user_id = %s'''

        (id, first_name, middle_name, last_name) = database.fetch(query, (handle, user_id))

        return Roommate(id, handle, user_id, first_name, middle_name, last_name)

    def get_allergies(self, id):
        '''Get a list of allergies for a person.'''
        query = '''SELECT allergies.id, allergies.name
                     FROM allergies
                          INNER JOIN roommates_allergies
                             ON allergy.id = roommates_allergies.allergy_id
                    WHERE roommate_id  = %s'''

        allergies = []

        for (id, name) in database.fetch_all(query, id):
            allergies.append(Allergies(id, name))

        return allergies

    def get_preferences(self, id):
        '''Fetch a list of all ingredients from the person.'''
        query = '''SELECT ingredients.id, ingredients.name
                     FROM ingredients
                          INNER JOIN roommates_preferences
                             ON ingredient.id = person_ingredient_relation.ingredient_id
                    WHERE roommate_id  = %s'''

        preferences = []

        for (id, name) in database.fetch_all(query, id):
            preferences.append(Ingredient(id, name))

        return preferences

    def get_count(self):
        '''Fetch the highest person id for a given user. This is used to
        genereate a index for a person.
        '''
        user_id = session['user']

        query = '''SELECT MAX(handle) AS count
                     FROM roommates
                    WHERE user_id = %s'''

        return database.fetch(query, user_id)[0]

    def get_roommates(self):
        '''Fetch a list of all persons.'''
        user_id = session['user']

        query = '''SELECT id, handle, first_name, middle_name, last_name
                     FROM roommates
                    WHERE user_id = %s
                 ORDER BY handle'''

        roommates = []

        for (id, handle, first_name, middle_name, last_name) in database.fetch_all(query, user):
            roommates.append(Roommate(id, handle, user_id, first_name, middle_name, last_name))

        return roommates
