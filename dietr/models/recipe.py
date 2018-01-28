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


class RecipeModel:
    @property
    def highest_id(self):
        """Fetch the highest id in the database"""
        return int(self.get_highest_id()['id'])


    @property
    def lowest_id(self):
        """Fetch the highest id in the database"""
        return int(self.get_lowest_id()['id'])


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
    @property
    def user_allergies(self):
        return tuple([allergy.id for allergy in self.user.allergies])

    def get_recipe(self, allergy_tuple, start, limit):

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
        query = '''SELECT name FROM extra_info
                    WHERE id IN (SELECT extra_info_id FROM recipes_extra_info WHERE recipe_id = %s)'''

        return database.fetch(query, recipe_id)

    def get_image(self, recipe_id):
        query = '''SELECT url FROM images
                    WHERE id IN (SELECT recipes.image_id FROM recipes WHERE id = %s)'''

        return database.fetch(query, recipe_id)['url']

    def get_ingredients(self, recipe_id):
        """Get all ingredients from the database and return a list of instances
        of the ingredient class.
        """
        query = '''SELECT id, name FROM ingredients
                    WHERE id IN (SELECT ingredient_id FROM recipes_ingredients WHERE recipe_id = %s)'''

        ingredients = database.fetch_all(query, recipe_id)

        # Convert the list of dicts to a list of ingredient objects
        return [Ingredient(**ingredient) for ingredient in ingredients]


    def get_allergies(self, ingredient_id):
        """Get all allergies from the database and return a list of instances
        of the allergy class.
        """
        query = '''SELECT id, name FROM allergies
                    WHERE id IN (SELECT allergy_id FROM allergies_ingredients WHERE ingredient_id = %s)'''

        allergies = database.fetch_all(query, ingredient_id)

        # Convert the list of dicts to a list of allergy objects
        return [Allergy(**allergy) for allergy in allergies]


    def get_lowest_id(self):
        """Find the lowest recipe in the database """
        query ='''SELECT id
                    FROM recipes
                   ORDER BY id
                   LIMIT 1'''

        return database.fetch(query)

    def complete_recipes(self, limit, start):
        """Return a list of recipes that is okay for the user to eat."""

        recipes = self.get_recipe(self.user_allergies, start, limit)

        #Add information
        for recipe in recipes:

            # Add the source of the recipe
            recipe.source = self.get_source(recipe.url)

            #Add the extra information
            recipe.extra_info = self.get_extra_info(recipe.id)

            #Add the image
            recipe.image = self.get_image(recipe.id)

            #Add all the ingredients contained in the recipe
            recipe.ingredients = self.get_ingredients(recipe.id)

            # Add all the allergens contained in the ingredients
            for ingredient in recipe.ingredients:
                allergens = self.get_allergies(ingredient.id)
                if allergens:
                    recipe.allergies += allergens

        return recipes

    def get_source(self, url):
        if 'http://www.jumbo.com:80/' in url:
            return 'Jumbo Supermarkten'

        else:
            return 'Albert Heijn'
