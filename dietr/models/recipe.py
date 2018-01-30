from dataclasses import dataclass, field
from enum import Enum

from dietr.database import database
from dietr.models.allergy import Allergy
from dietr.models.ingredient import Ingredient

'''
SELECT COUNT(*) AS recipe_count
  FROM recipes
 WHERE recipes.id NOT IN (SELECT recipe_id
                            FROM recipes_allergies
                           WHERE allergy_id IN (0))
   AND recipes.id NOT IN (SELECT recipe_id
                            FROM recipes_ingredients
                           WHERE ingredient_id IN (0))
   AND recipes.id NOT IN (SELECT recipe_id
                            FROM recipes_tags
                           WHERE tag_id IN (0));

SELECT recipes.id, recipes.name, recipes.url,
       images.url AS image
  FROM recipes
 INNER JOIN images
    ON recipes.image_id = images.id
 WHERE recipes.id NOT IN (SELECT recipe_id
                            FROM recipes_allergies
                           WHERE allergy_id IN (0))
   AND recipes.id NOT IN (SELECT recipe_id
                            FROM recipes_ingredients
                           WHERE ingredient_id IN (0))
   AND recipes.id NOT IN (SELECT recipe_id
                            FROM recipes_tags
                           WHERE tag_id IN (0))
 ORDER BY recipes.name ASC
 LIMIT 0, 20;
'''


class Order(Enum):
    ASCENDING = 1
    DESCENDING = 2


@dataclass
class Recipe:
    id: int
    name: str
    url: str
    image: str
    allergies: list = field(default_factory=list, init=False)
    ingredients: list = field(default_factory=list, init=False)
    tags: str = field(default_factory=str, init=False)

    @property
    def source(self):
        """Find's the source using a provided url."""
        if 'http://www.jumbo.com:80/' in self.url:
            return 'Jumbo Supermarkten'

        else:
            return 'Albert Heijn'


@dataclass
class Tag:
    id: int
    name: str


class RecipeModel:
    def get_recipes(self, allergies, preferences, tags, order, start, limit):
        """Fetch all the initial information for the recipes excluding recipes
        that have one of the user allergies.
        """
        query = f'''SELECT recipes.id, recipes.name, recipes.url,
                           images.url AS image
                      FROM recipes
                     INNER JOIN images
                        ON recipes.image_id = images.id
                     WHERE recipes.id NOT IN (SELECT recipe_id
                                                FROM recipes_allergies
                                               WHERE allergy_id IN %s)
                       AND recipes.id NOT IN (SELECT recipe_id
                                                FROM recipes_ingredients
                                               WHERE ingredient_id IN %s)
                       AND recipes.id NOT IN (SELECT recipe_id
                                                FROM recipes_tags
                                               WHERE tag_id IN %s)
                     ORDER BY recipes.name {order}
                     LIMIT %s, %s'''

        # Prefent passing a empy list, instead pass a non-existing id
        if not allergies:
            allergies = [0]

        if not preferences:
            preferences = [0]

        if not tags:
            tags = [0]

        recipes = database.fetch_all(query, (allergies, preferences, tags,
                                             start, limit))

        return [Recipe(**recipe) for recipe in recipes]

    def get_recipe_count(self, allergies, preferences, tags):
        """Fetch the total number of recipes excluding the recipes that contain
        a user allergy.
        """
        query = f'''SELECT COUNT(*) AS recipe_count
                      FROM recipes
                     WHERE recipes.id NOT IN (SELECT recipe_id
                                                FROM recipes_allergies
                                               WHERE allergy_id IN %s)
                       AND recipes.id NOT IN (SELECT recipe_id
                                                FROM recipes_ingredients
                                               WHERE ingredient_id IN %s)
                       AND recipes.id NOT IN (SELECT recipe_id
                                                FROM recipes_tags
                                               WHERE tag_id IN %s)'''

        # Prefent passing a empy list, instead pass a non-existing id
        if not allergies:
            allergies = [0]

        if not preferences:
            preferences = [0]

        if not tags:
            tags = [0]

        result = database.fetch(query, (allergies, preferences, tags))

        return result['recipe_count']

    def get_tags(self, recipe_id):
        """Fetch all the extra info for a recipe (eg. main dish, desert, vegan)"""
        query = '''SELECT id, name
                     FROM tags
                    WHERE id IN (SELECT tag_id
                                   FROM recipes_tags
                                  WHERE recipe_id = %s)'''

        tags = database.fetch_all(query, recipe_id)

        # Convert the list of dicts to a list of tag objects
        return [Tag(**tag) for tag in tags]

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

    def get_allergies(self, recipe_id):
        """Get all allergies from the database and return a list of instances
        of the allergy class.
        """
        query = '''SELECT DISTINCT id, name FROM allergies
                    WHERE id IN (SELECT allergy_id
                                     FROM allergies_ingredients
                                    WHERE ingredient_id IN (SELECT ingredient_id
                                                                FROM recipes_ingredients
                                                                WHERE recipe_id = %s))'''

        allergies = database.fetch_all(query, recipe_id)

        # Convert the list of dicts to a list of allergy objects
        return [Allergy(**allergy) for allergy in allergies]
