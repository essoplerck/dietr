from .. import connection

class PersonModel:
    '''Model for the person pages. This model will handle all ineractions
    with the database.
    '''
    def add_person(self, person):
        pass

    def edit_person(self, person):
        pass

    def delete_person(self, name):
        pass

    def get_person(self, name):
        user_id = 1

        query = '''SELECT *
                     FROM person
                    WHERE account_id = %s
                      AND name = %s'''

        cursor = connection.cursor()
        cursor.execute(query, (user_id, name))

        person = cursor.fetchone()

        return person

    def get_allergies(self, id):
        query = '''SELECT category.id, category.name
                     FROM category
                          INNER JOIN person_category_relation
                                  ON category.id = person_category_relation.category_id
                    WHERE person_id = %s'''

        cursor = connection.cursor()
        cursor.execute(query, id)

        allergens = cursor.fetchall()

        return allergens

    def get_ingredients(self, id):
        query = '''SELECT ingredient.id, ingredient.name
                     FROM ingredient
                          INNER JOIN person_ingredient_relation
                                  ON ingredient.id = person_ingredient_relation.ingredient_id
                    WHERE person_id = %s'''

        cursor = connection.cursor()
        cursor.execute(query, id)

        allergens = cursor.fetchall()

        return allergens

    def get_persons(self):
        user_id = 1

        query = '''SELECT *
                     FROM person
                    WHERE account_id = %s'''

        cursor = connection.cursor()
        cursor.execute(query, user_id)

        persons = cursor.fetchall()

        return persons
