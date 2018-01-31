from dataclasses import dataclass, field

from flask import session

from dietr.database import database
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
    def add_roommate(self, user_id, first_name, middle_name, last_name):
        """Add a roommate to the database."""
        handle = self.get_handle(user_id)

        if not handle:
            handle = 1

        query = '''INSERT INTO roommates (handle, user_id, first_name,
                                          middle_name, last_name)
                   VALUES (%s, %s, %s, %s, %s)'''

        database.commit(query, (handle, user_id, first_name, middle_name,
                                last_name))

    def delete_roommate(self, id):
        """Delete a roomate from the database."""
        query = '''DELETE FROM roommates
                    WHERE id = %s'''

        database.commit(query, id)

    def get_allergies(self, id):
        """Get all allergies for a roommate from the database and return a list
        of instances of the allergy class.
        """
        query = '''SELECT allergies.id, allergies.name
                     FROM allergies, roommates_allergies AS ra
                    WHERE ra.roommate_id = %s
                      AND ra.allergy_id = allergies.id'''

        allergies = database.fetch_all(query, id)

        # Convert the list of dicts to a list of allergy objects
        return [Allergy(**allergy) for allergy in allergies]

    def get_handle(self, user_id):
        """Get the highest roommate id for an user. This is used to genereate a
        handle for a roommate.
        """
        query = '''SELECT MAX(handle) + 1 AS handle
                     FROM roommates
                    WHERE user_id = %s'''

        # Return the
        return database.fetch(query, user_id)['handle']

    def get_preferences(self, id):
        """Get all preferences for a roommate from the database and return a
        listof instances of the ingredient class.
        """
        query = '''SELECT ingredients.id, ingredients.name
                     FROM ingredients, roommates_preferences AS rp
                    WHERE rp.roommate_id = %s
                      AND rp.ingredient_id = ingredients.id'''

        preferences = database.fetch_all(query, id)

        # Convert the list of dicts to a list of ingredient objects
        return [Ingredient(**ingredient) for ingredient in preferences]

    def get_roommate(self, user_id, handle):
        """Get a roommate from the database and return an instance of the
        roommate class.
        """
        query = '''SELECT id, handle,
                          user_id,
                          first_name, middle_name, last_name
                     FROM roommates
                    WHERE handle = %s
                      AND user_id = %s'''

        # Convert dict to a roommate object
        return Roommate(**database.fetch(query, (handle, user_id)))

    def get_roommates(self, user_id):
        """Get all roommates for a user from the database and return a list of
        instances of the roommate class.
        """
        query = '''SELECT id, handle,
                          user_id,
                          first_name, middle_name, last_name
                     FROM roommates
                    WHERE user_id = %s
                 ORDER BY handle'''

        roommates = database.fetch_all(query, user_id)

        # Convert the list of dicts to a list of roommate objects
        return [Roommate(**roommate) for roommate in roommates]

    def set_roommate(self, id, first_name, middle_name, last_name):
        """Set the name of a roommate."""
        query = '''UPDATE roommates
                      SET first_name = %s,
                          middle_name = %s,
                          last_name = %s
                    WHERE id = %s'''

        database.commit(query, (first_name, middle_name, last_name, id))
