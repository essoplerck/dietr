from dataclasses import dataclass, field

from dietr.database import database
from dietr.models.allergy import Allergy
from dietr.models.ingredient import Ingredient


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
        """Find's the source using a provided url."""
        if 'http://www.jumbo.com:80/' in self.url:
            return 'Jumbo Supermarkten'

        else:
            return 'Albert Heijn'


class RecipeModel:
    def get_recipes(self, allergy_tuple, start, limit):
        """Fetch all the initial information for the recipes excluding recipes
        that have one of the user allergies.
        """
        query = '''SELECT recipes.id, recipes.name, recipes.url
                     FROM recipes
                    WHERE recipes.id
                      NOT IN (SELECT recipe_id
                                FROM recipes_ingredients AS ri
                               INNER JOIN allergies_ingredients AS ai
                                  ON ai.ingredient_id = ri.ingredient_id
                               WHERE ai.allergy_id IN %s)
                    LIMIT %s, %s'''

        recipes = database.fetch_all(query, (allergy_tuple, start, limit))

        return [Recipe(**recipe) for recipe in recipes]

    def get_recipe_count(self, allergy_tuple):
        """Fetch the total number of recipes excluding the recipes that contain
        a user allergy.
        """
        if not allergy_tuple:
            query = '''SELECT COUNT(*) AS recipe_count
                         FROM recipes'''

            return database.fetch(query)['recipe_count']

        else:
            query = '''SELECT COUNT(*) AS recipe_count
                         FROM recipes
                        WHERE recipes.id
                          NOT IN (SELECT recipe_id
                                    FROM recipes_ingredients AS ri
                                   INNER JOIN allergies_ingredients AS ai
                                      ON ai.ingredient_id = ri.ingredient_id
                                   WHERE ai.allergy_id IN %s)'''

            return database.fetch(query, (allergy_tuple,))['recipe_count']

    def get_extra_info(self, recipe_id):
        """Fetch all the extra info for a recipe (eg. main dish, desert, vegan)"""
        query = '''SELECT name
                     FROM extra_info
                    WHERE id IN (SELECT extra_info_id
                                   FROM recipes_extra_info
                                  WHERE recipe_id = %s)'''

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
        query = '''SELECT id, name
                     FROM ingredients
                    WHERE id IN (SELECT ingredient_id
                                   FROM recipes_ingredients
                                  WHERE recipe_id = %s)'''

        ingredients = database.fetch_all(query, recipe_id)

        # Convert the list of dicts to a list of ingredient objects
        return [Ingredient(**ingredient) for ingredient in ingredients]

    def get_allergies(self, ingredient_id):
        """Get all allergies from the database and return a list of instances
        of the allergy class.
        """
        query = '''SELECT id, name
                     FROM allergies
                    WHERE id IN (SELECT allergy_id
                                   FROM allergies_ingredients
                                  WHERE ingredient_id = %s)'''

        allergies = database.fetch_all(query, ingredient_id)

        # Convert the list of dicts to a list of allergy objects
        return [Allergy(**allergy) for allergy in allergies]
