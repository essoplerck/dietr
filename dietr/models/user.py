from dataclasses import dataclass, field

from flask import session
from passlib.hash import sha256_crypt as sha256

from dietr.database import database
from dietr.models.allergy import Allergy
from dietr.models.ingredient import Ingredient


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

    @property
    def name(self):
        if self.middle_name:
            return f'{self.first_name} {self.middle_name} {self.last_name}'

        else:
            return f'{self.first_name} {self.last_name}'


class UserModel:
    def add_user(self, username, email, first_name, middle_name, last_name,
                 password):
        """Add a user to the database."""
        pass

    def generate_hash(self, password):
        """Generate a sha256 hash of a password."""
        return sha256.hash(password)

    def get_allergies(self, user_id):
        """Get a list of allergies of an user from the database and return a
        list of instances of the allergy class.
        """
        query = '''SELECT allergies.id, allergies.name
                     FROM allergies, users_allergies
                    WHERE users_allergies.user_id = %s
                      AND users_allergies.allergy_id = allergies.id'''

        allergies = database.fetch_all(query, user_id)

        # Convert the list of dicts to a list of allergy objects
        if allergies:
            return [Allergy(**allergy) for allergy in allergies]

    def get_preferences(self, user_id):
        """Get a list of preferences of a user from the database and return a
        list of instances of the ingredient class.
        """
        query = '''SELECT ingredients.id, ingredients.name
                     FROM ingredients, users_preferences
                    WHERE users_preferences.user_id = %s
                      AND users_preferences.ingredient_id = ingredients.id'''

        ingredients = database.fetch_all(query, user_id)

        # Convert the list of dicts to a list of ingredients objects
        return [Ingredient(**ingredient) for ingredient in ingredients]

    def get_user(self, id):
        """Get an user from the database and return an instance of the user
        class.
        """
        query = '''SELECT id,
                          username,
                          email,
                          first_name, middle_name, last_name,
                          hash
                     FROM users
                    WHERE id = %s'''

        # Convert dict to an user object
        return User(**database.fetch(query, id))

    def get_user_by_username(self, username):
        """Get an user from the database and return an instance of the user
        class.
        """
        query = '''SELECT id,
                          username,
                          email,
                          first_name, middle_name, last_name,
                          hash
                     FROM users
                    WHERE username = %s'''

        # Convert dict to an user object
        return User(**database.fetch(query, username))

    def set_email(self, id, email):
        """Set the email adress of the user."""
        query = '''UPDATE users
                      SET email = %s
                    WHERE id = %s;'''

        database.commit(query, (mail, id))

    def set_name(self, id, first_name, middle_name, last_name):
        """Set  the name of the user."""
        query = '''UPDATE users
                      SET first_name = %s,
                          middle_name = %s,
                          last_name = %s
                    WHERE id = %s;'''

        database.commit(query, (first_name, middle_name, last_name, id))

    def set_password(self, id, password):
        """Set the user password."""
        hash = self.generate_hash(password)

        query = '''UPDATE users
                      SET hash = %s
                    WHERE id = %s;'''

        database.commit(query, (hash, id))

    def set_username(self, id, username):
        """Set the username of the user."""
        query = '''UPDATE users
                      SET username = %s
                    WHERE id = %s;'''

        database.commit(query, (username, id))

    def verify_email(self, email):
        """Check if the email adress is valid and if it is not in use."""
        # @TODO vefify email adress
        query = '''SELECT COUNT(email) AS email_count
                     FROM users
                    WHERE email = %s'''

        # Retrun number of matching email adresses
        return database.fetch(query, email)['email_count']

    def verify_password(self, password, hash):
        """Check if the password matches the hash."""
        return sha256.verify(password, hash)

    def verify_username(self, username):
        """Check if the username is valid and if it is not in use."""
        query = '''SELECT COUNT(username) AS username_count
                     FROM users
                    WHERE username = %s'''

        # Retrun number of matching usernames
        return database.fetch(query, username)['username_count']
