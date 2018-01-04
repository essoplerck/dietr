from .. import connection

class PersonModel:
    '''Model for the person pages. This model will handle all ineractions
    with the database.
    '''
    def add_person(self, person):
        user_id = 1

        query = '''INSERT INTO person (account_id, name, url)
                        VALUES (%s, %s, %s)'''

        cursor = connection.cursor()
        cursor.execute(query, (user_id, person['name'], person['url']))

        # Execute query
        connection.commit()

    def edit_person(self, person):
        user_id = 1

        query = '''UPDATE person
                      SET name       = %s,
                          url        = %s
                    WHERE id         = %s
                      AND account_id = %s'''

        cursor = connection.cursor()
        cursor.execute(query, (person['name'], person['url'], person['name'],
                                                              user_id))

        # Execute query
        connection.commit()

    def remove_person(self, id):
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM person
                                WHERE person.id = %s''', id)

        cursor.execute('''DELETE FROM person_category_relation
                                WHERE person_id = %s''', id)

        cursor.execute('''DELETE FROM person_ingredient_relation
                                WHERE person_ingredient_relation.person_id = %s''', id)

        # Execute query
        connection.commit()

    def get_person(self, url):
        user_id = 1

        query = '''SELECT *
                     FROM person
                    WHERE account_id = %s
                      AND url = %s'''

        cursor = connection.cursor()
        cursor.execute(query, (user_id, url))

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
