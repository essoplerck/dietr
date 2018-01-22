from flask import session

from dietr.database import database
from dietr.models.allergy import Allergy
from dietr.models.ingredient import Ingredient
from dietr.models.user import UserModel


class DietModel(UserModel):
    def get_allergies(self):
        """Get all allergies for an user from the database and return a list of
        instances of the allergy class.
        """
        user_id = session['user']

        query = '''SELECT allergies.id, allergies.name
                     FROM allergies, users_allergies AS ua
                    WHERE ua.user_id = %s
                      AND ua.allergy_id = allergies.id'''

        allergies = database.fetch_all(query, user_id)

        # Convert the list of dicts to a list of allergy objects
        return [Allergy(**allergy) for allergy in allergies]

    def get_preferences(self):
        """Get all preferences for a roommate from the database and return a
        listof instances of the ingredient class.
        """
        user_id = session['user']

        query = '''SELECT ingredients.id, ingredients.name
                     FROM ingredients, users_preferences AS up
                    WHERE up.user_id = %s
                      AND up.ingredient_id = ingredients.id'''

        preferences = database.fetch_all(query, user_id)

        # Convert the list of dicts to a list of ingredient objects
        return [Ingredient(**ingredient) for ingredient in preferences]
