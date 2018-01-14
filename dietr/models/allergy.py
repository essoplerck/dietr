from dataclasses import dataclass


@dataclass
class Allergy:
    id: int
    name: str


class AllergyModel:
    def add_allergy(self, name):
        query = '''INSERT INTO allergies (name)
                   VALUES (%s)'''

        # Execute query
        database.commit(query, name)

    def delete_allergy(self, id):
        query = '''DELETE FROM allergies
                    WHERE id = %s'''

        # Execute query
        database.commit(query, id)

    def get_allergy(self, id):
        query = '''SELECT id, name
                     FROM allergies
                    WHERE id = %s'''

        return Allergy(**database.fetch(query, id))

    def get_allergies(self):
        query = '''SELECT id, name
                     FROM allergies
                    ORDER BY name'''

        allergies = database.fetch_all(query)

        return [Allergy(**allergy) for allergy in allergies]

    def set_allergy(self, id, name):
        query = '''UPDATE allergies
                      SET name = %s
                    WHERE id = %s'''

        # Execute query
        database.commit(query, (name, id))
