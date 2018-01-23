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
    extra: str
    image: str
    source: str = field(default_factory=str, init=False)
    allergies: list = field(default_factory=list, init=False)
    ingredients: list = field(default_factory=list, init=False)

    def __post_init__(self):
        if self.image is None:
            self.image = None

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

        user = user_model.get_user()
        user.allergies = user_model.get_allergies(user.id)
        #user.preferences = user.get_preferences(user.id)
        user.roommates = roommate_model.get_roommates()

        if user.roommates:
            for roommate in user.roommates:
                roommate.allergies = roommate_model.get_allergies(roommate.id)
                #roommate.get_preferences(roommate.id)
        return user

    def get_recipe(self, start, stop):
        """Fetch initial recipe value's """
        query = '''SELECT
                    recipes.id as id,
                    recipes.name as name,
                    recipes.url as url,
                    images.url as image,
                    extra_info.name as extra
                FROM recipes, images, recipes_extra_info, extra_info
                WHERE recipes.image_id = images.id
                AND recipes_extra_info.extra_info_id = extra_info.id
                AND recipes_extra_info.recipe_id = recipes.id
                AND recipes.id >= %s
                ORDER BY recipes.id
                LIMIT %s'''
        recipes = database.fetch_all(query, (start, stop))

        return [Recipe(**recipe) for recipe in recipes]

    def get_recipe_count(self):
        query = '''SELECT COUNT(*) from recipes'''

        return database.fetch(query)


    def get_lowest_id(self):
        """Find the lowest recipe in the database """
        query ='''SELECT id FROM recipes ORDER BY id LIMIT 1'''

        return database.fetch(query)

    def get_highest_id(self):
        """Order all the id's in descending order and fetch one, i.e. the highest/last recipe"""
        query = '''SELECT id FROM recipes ORDER BY id DESC LIMIT 1'''

        return database.fetch(query)

    def get_ingredients(self, recipe_id):
        """Get all ingredients from the database and return a list of instances
        of the ingredient class.
        """
        query = '''SELECT ingredients.id as id, ingredients.name as name
                     FROM ingredients, recipes_ingredients
                     WHERE ingredients.id = recipes_ingredients.ingredient_id
                     AND recipes_ingredients.recipe_id = %s
                    ORDER BY name'''

        ingredients = database.fetch_all(query, recipe_id)

        # Convert the list of dicts to a list of ingredient objects
        return [Ingredient(**ingredient) for ingredient in ingredients]

    def get_allergies(self, ingredient_id):
        """Get all allergies from the database and return a list of instances
        of the allergy class.
        """
        query = '''SELECT allergies.id as id,
                        allergies.name as name
                     FROM allergies
                     INNER JOIN allergies_ingredients on allergies_ingredients.allergy_id = allergies.id
                     WHERE allergies_ingredients.ingredient_id = %s
                    ORDER BY name'''

        allergies = database.fetch_all(query, ingredient_id)

        # Convert the list of dicts to a list of allergy objects
        return [Allergy(**allergy) for allergy in allergies]



    #
    # def get_recipe_id(self, name):
    #     """Fetch all recipe_id's that contain name"""
    #     query = '''SELECT id FROM recipes WHERE name LIKE %s'''
    #
    #     return database.fetch_all(query, f'%{name}%')




    def create_list(self, limit, start):
        """Checks whether the returned list is long enough"""
        start_recipe = start

        recipes = self.check_all_recipes(limit, start)

        while len(recipes) < limit and recipes[-1].id < self.highest_id:
            print(len(recipes))
            start_recipe += limit
            recipes += self.check_all_recipes(limit, start_recipe)

        return recipes


    def user_is_allergic(self, allergy_ids, user_allergies = None, roommate_allergies = None):
        """Returns true when the user has an allergy for an ingredient contained within a recipe"""
        #Check to see if the user has any allergies at all
        if (user_allergies or roommate_allergies) and (user_allergies == list or roommate_allergies == list):
            #Check if any user_allergie is contained within the recipe and return true
            for allergy in (user_allergies or roommate_allergies):
                if allergy.id in allergy_ids:
                    return True

        return False


    def check_all_recipes(self, limit, start):
        """Return a list of recipes that is okay for the user to eat."""

        checked_recipes = []

        #Fetch recipes starting with 'start' and ending 'limit + 5' after start
        #Fetches a couple of more recipes to account for some empty id's
        recipes = self.get_recipe(start, limit)
        print (recipes)

        for recipe in recipes:

            #Checks whether the list reached the specified limit and if the counter doesn't pick a non-excistng recipe
            if len(checked_recipes) >= limit:
                break

            #Add all the information that wasn't provided yet

            #Add the source of the recipe
            recipe.source = self.get_source(recipe.url)

            #Add all the ingredients contained in the recipe
            recipe.ingredients = self.get_ingredients(recipe.id)

            #Add all the allergens contained in the ingredients
            for ingredient in recipe.ingredients:
                allergens = self.get_allergies(ingredient.id)
                if allergens:
                    recipe.allergies += allergens

            #Provide a value for the allergies if none is provided, AAANPASSEN
            if not recipe.allergies:
                recipe.allergies = [Allergy(None, 'Geen allergenen')]
                checked_recipes.append(recipe)
                continue

            #If the user isn't logged in add the recipe without checking for allergies, YET!!!
            if not self.user:
                checked_recipes.append(recipe)
                continue

            if not self.user_is_allergic(recipe.allergies, user_allergies = self.user.id) and \
            not self.user_is_allergic(recipe.allergies, roommate_allergies = (roommate.allergies for roommate in self.user.roommates)):
                checked_recipes.append(recipe)

        return checked_recipes


    def get_source(self, url):
        if "http://www.jumbo.com:80/" in url:
            return "Jumbo Supermarkten"
        else:
            return "Albert Heijn"
