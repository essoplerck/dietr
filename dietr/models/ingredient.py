from dataclasses import dataclass, field

from dietr.database import database
from dietr.models.allergy import Allergy


@dataclass
class Ingredient:
    id: int
    name: str
    allergens: list = field(default_factory=list, init=False)


class IngredientModel:
    """Handles all interaction with the database."""
    def add_ingredient(self, name):
        """Add an ingredient to the database."""
        query = '''INSERT INTO ingredients (name)
                   VALUES (%s)'''

        # Execute query
        database.commit(query, name)

    def delete_ingredient(self, id):
        """Delete an ingredient from the database."""
        query = '''DELETE FROM ingredients
                    WHERE id = %s'''

        # Execute query
        database.commit(query, id)

    def get_ingredient(self, id):
        """Get an ingredient from the database and return an instance of the
        ingredient class.
        """
        query = '''SELECT id, name
                     FROM ingredients
                    WHERE id = %s'''

        # Convert dict to an ingredient object
        return Ingredient(**database.fetch(query, id))

    def get_allergens(self, id):
        """Get all allergens for a ingredient from the database and return a
        list of instances of the allergy class.
        """
        query = '''SELECT allergies.id, allergies.name
                     FROM allergies
                          INNER JOIN allergies_ingredients
                          ON allergies.id = allergies_ingredients.allergy_id
                   WHERE ingredient_id = %s'''

        allergens = database.fetch_all(query, id)

        # Convert the list of dicts to a list of allergy objects
        return [Allergy(**allergen) for allergen in allergens]

    def get_ingredients(self):
        """Get all ingredients from the database and return a list of instances
        of the ingredient class.
        """
        query = '''SELECT id, name
                     FROM ingredients
                    ORDER BY name'''

        ingredients = database.fetch_all(query)

        # Convert the list of dicts to a list of ingredient objects
        return [Ingredient(**ingredient) for ingredient in ingredients]

    def set_ingredient(self, id, name):
        """Set the name of an ingredient."""
        query = '''UPDATE ingredients
                      SET name = %s
                    WHERE id = %s'''

        # Execute query
        database.commit(query, (name, id))
