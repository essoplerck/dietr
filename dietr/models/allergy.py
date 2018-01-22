from dataclasses import dataclass

from dietr.database import database


@dataclass
class Allergy:
    id: int
    name: str


class AllergyModel:
    def add_allergy(self, name):
        """Add an allergy to the database."""
        query = '''INSERT INTO allergies (name)
                   VALUES (%s)'''

        database.commit(query, name)

    def delete_allergy(self, id):
        """Delete an allergy from the database."""
        query = '''DELETE FROM allergies
                    WHERE id = %s'''

        database.commit(query, id)

    def get_allergy(self, id):
        """Get an allergy from the database and return an instance of the
        allergy class.
        """
        query = '''SELECT id, name
                     FROM allergies
                    WHERE id = %s'''

        # Convert dict to an allergy object
        return Allergy(**database.fetch(query, id))

    def get_allergies(self):
        """Get all allergies from the database and return a list of instances
        of the allergy class.
        """
        query = '''SELECT id, name
                     FROM allergies
                    ORDER BY name'''

        allergies = database.fetch_all(query)

    def get_ingredient_allergies(self, ingredient_id):
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

    def set_allergy(self, id, name):
        """Set the name of an allergy."""
        query = '''UPDATE allergies
                      SET name = %s
                    WHERE id = %s'''

        database.commit(query, (name, id))
