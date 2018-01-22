from dataclasses import dataclass, field

from flask import session

from dietr.database import database
from dietr.models.allergy import Allergy


@dataclass
class User:
    id: int
    username: str
    email: str
    first_name: str
    middle_name: str
    last_name: str
    hash: str
    allergies: list = field(default_factory=list, init=False)
    roommates: list = field(default_factory=list, init=False)
    preferences: list = field(default_factory=list, init=False)
    roommates: list = field(default_factory=list, init=False)

    @property
    def name(self):
        if self.middle_name:
            return f'{self.first_name} {self.middle_name} {self.last_name}'

        else:
            return f'{self.first_name} {self.last_name}'


class UserModel:
    def get_user(self):
        """Get a user form the database."""
        user_id = session['user']

        query = '''SELECT id,
                          username,
                          email,
                          first_name, middle_name, last_name,
                          hash
                     FROM users
                    WHERE id = %s'''

        # Convert dict to an user object
        return User(**database.fetch(query, user_id))

    def get_allergies(self, id):
        """Get all allergies for a user from the database and return a list
        of instances of the allergy class.
        """
        query = '''SELECT allergies.id, allergies.name
                     FROM allergies, users_allergies
                    WHERE users_allergies.user_id = %s
                      AND users_allergies.allergy_id = allergies.id'''

        allergies = database.fetch_all(query, id)

        # Convert the list of dicts to a list of allergy objects
        if allergies:
            return [Allergy(**allergy) for allergy in allergies]
        return None
