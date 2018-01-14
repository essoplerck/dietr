from dataclasses import dataclass

from dietr.database import database


@dataclass
class Allergy:
    id: int
    name: str


class AllergyModel:
    """Handles all interaction with the database."""
    def add_allergy(self, name):
        """Adds an allergy to the database."""
        query = '''INSERT INTO allergies (name)
                   VALUES (%s)'''

        # Execute query
        database.commit(query, name)

    def delete_allergy(self, id):
        """Deletes an allergy from the database."""
        query = '''DELETE FROM allergies
                    WHERE id = %s'''

        # Execute query
        database.commit(query, id)

    def get_allergy(self, id):
        """Gets an allergy from the database."""
        query = '''SELECT id, name
                     FROM allergies
                    WHERE id = %s'''

        # Convert dict to allergy object
        return Allergy(**database.fetch(query, id))

    def get_allergies(self):
        """Gets a list of all allergies from the database."""
        query = '''SELECT id, name
                     FROM allergies
                    ORDER BY name'''

        allergies = database.fetch_all(query)

        # Convert the list of dicts to a list of allergy object
        return [Allergy(**allergy) for allergy in allergies]

    def set_allergy(self, id, name):
        """Sets the name of an allergy."""
        query = '''UPDATE allergies
                      SET name = %s
                    WHERE id = %s'''

        database.commit(query, (name, id))
