from dataclasses import dataclass, field

from flask import session

from dietr.database import database

from dietr.models.roommate import RoommateModel
from dietr.models.user import UserModel
from dietr.models.ingredient import Ingredient
from dietr.models.allergy import Allergy

#Contains all the necessary database calls
roommate_model = RoommateModel()
user_model = UserModel()



@dataclass
class Recipe:
    id: int
    name: str
    url: str
    extra: str = field(default_factory=str, init=False)
    image: str = field(default_factory=str, init=False)
    source: str = field(default_factory=str, init=False)
    allergies: list = field(default_factory=list, init=False)
    ingredients: list = field(default_factory=list, init=False)

    @property
    def get_source(self):
        """Find's the source using a provided url"""
        if 'http://www.jumbo.com:80/' in self.url:
            return 'Jumbo Supermarkten'

        else:
            return 'Albert Heijn'

class RecipeModel:
    @property
    def user(self):
        """Fetch all the user information"""
        if 'user' not in session:
            return None


        user = user_model.get_user()
        user.allergies = user_model.get_allergies(user.id)
        #user.preferences = user.get_preferences(user.id)
        user.roommates = roommate_model.get_roommates()

        if user.roommates:
            for roommate in user.roommates:
                roommate.allergies = roommate_model.get_allergies(roommate.id)
                #roommate.get_preferences(roommate.id)
        return user


    def user_allergies(self, roommate_allergies):
        """Converts the user allergies from a dataclass to a tuple of id's"""
        allergies = [allergy.id for allergy in self.user.allergies]
        if roommate_allergies:
            allergies += roommate_allergies

        return tuple(allergies)

    def get_recipe(self, allergy_tuple, start, limit):
        """Fetch all the initial information for the recipes excluding recipes that have one of the user allergies"""
        query = '''SELECT recipes.id,
                    recipes.name,
                    recipes.url

                    FROM recipes

                    WHERE recipes.id NOT IN
                    (SELECT recipe_id FROM recipes_ingredients
                    INNER JOIN allergies_ingredients
                    ON allergies_ingredients.ingredient_id = recipes_ingredients.ingredient_id
                    WHERE allergies_ingredients.allergy_id IN %s)

                    LIMIT %s, %s'''

        recipes = database.fetch_all(query, (allergy_tuple, start, limit))

        return [Recipe(**recipe) for recipe in recipes]


    def get_recipe_count(self, allergy_tuple):
        """Fetch the total number of recipes excluding the recipes that contain a user allergy"""

        if not allergy_tuple:
            query = '''SELECT COUNT(*) FROM recipes'''
            count = database.fetch(query)
        else:
            query = '''SELECT COUNT(*)
                        FROM (SELECT id FROM recipes
                        WHERE recipes.id NOT IN
                        (SELECT recipe_id FROM recipes_ingredients
                        INNER JOIN allergies_ingredients
                        ON allergies_ingredients.ingredient_id = recipes_ingredients.ingredient_id
                        WHERE allergies_ingredients.allergy_id IN %s)) A'''

            count = database.fetch(query, (allergy_tuple,))

        return count['COUNT(*)']

    def get_extra_info(self, recipe_id):
        """Fetch all the extra info for a recipe (eg. main dish, desert, vegan)"""
        query = '''SELECT name FROM extra_info
                    WHERE id IN (SELECT extra_info_id FROM recipes_extra_info WHERE recipe_id = %s)'''

        return database.fetch(query, recipe_id)

    def get_image(self, recipe_id):
        """Fetches the image url"""
        query = '''SELECT url FROM images
                    WHERE id IN (SELECT recipes.image_id FROM recipes WHERE id = %s)'''

        return database.fetch(query, recipe_id)['url']

    def get_ingredients(self, recipe_id):
        """Fetch all ingredients from the database and return a list of instances
        of the ingredient class.
        """
        query = '''SELECT id, name FROM ingredients
                    WHERE id IN (SELECT ingredient_id FROM recipes_ingredients WHERE recipe_id = %s)'''

        ingredients = database.fetch_all(query, recipe_id)

        # Convert the list of dicts to a list of ingredient objects
        return [Ingredient(**ingredient) for ingredient in ingredients]


    def get_allergies(self, recipe_id):
        """Get all allergies from the database and return a list of instances
        of the allergy class.
        """
        query = '''SELECT DISTINCT id, name FROM allergies
                    WHERE id IN (SELECT allergy_id FROM allergies_ingredients WHERE ingredient_id IN
                               	(SELECT ingredient_id FROM recipes_ingredients WHERE recipe_id = %s))'''

        allergies = database.fetch_all(query, recipe_id)

        # Convert the list of dicts to a list of allergy objects
        return [Allergy(**allergy) for allergy in allergies]
