from .. import connection


class PersonModel:
    '''Model for the person pages. This model will handle all ineractions
    with the database.
    '''
    def add_person(self, person):
        '''Insert a person into the database.'''
        user_id = 1

        query = '''INSERT INTO person (id, name, user_id)
                        VALUES (%s, %s, %s)'''

        cursor = connection.cursor()
        cursor.execute(query, (person['name'], person['id'], user_id))

        # Execute query
        return connection.commit()

    def edit_person(self, person):
        '''Update a person in the database. Person id will be preserved.'''
        user_id = 1

        cursor = connection.cursor()
        cursor.execute('''UPDATE person
                             SET name       = %s,
                           WHERE id         = %s
                             AND user_id = %s''', (person['name'], person['id'],
                                                   user_id))

        # Execute query
        return connection.commit()

    def remove_person(self, id):
        '''Delete a person from the database. Will also remove related
        tables.
        '''
        user_id = 1

        cursor = connection.cursor()
        cursor.execute('''DELETE FROM person
                                WHERE id      = %s
                                  AND user_id = %s''', (id, user_id))

        cursor.execute('''DELETE FROM person_category_relation
                                WHERE person_id = %s
                                  AND user_id   = %s''', (id, user_id))

        cursor.execute('''DELETE FROM person_ingredient_relation
                                WHERE person_id = %s
                                  AND user_id   = %s''', (id, user_id))

        # Execute query
        return connection.commit()

    def get_person(self, id):
        '''Fetch a person from the database.'''
        user_id = 1

        query = '''SELECT *
                     FROM person
                    WHERE id      = %s
                      AND user_id = %s'''

        cursor = connection.cursor()
        cursor.execute(query, (index, user_id))

        # Return person
        return cursor.fetchone()

    def get_allergies(self, id):
        '''Get a list of allergies for a person.'''
        query = '''SELECT category.id, category.name
                     FROM category
                          INNER JOIN person_category_relation
                                  ON category.id = person_category_relation.category_id
                    WHERE person_id = %s'''

        cursor = connection.cursor()
        cursor.execute(query, id)

        # Return allergies
        return cursor.fetchall()

    def get_ingredients(self, id):
        '''Fetch a list of all ingredients from the person.'''
        query = '''SELECT ingredient.id, ingredient.name
                     FROM ingredient
                          INNER JOIN person_ingredient_relation
                                  ON ingredient.id = person_ingredient_relation.ingredient_id
                    WHERE person_id = %s'''

        cursor = connection.cursor()
        cursor.execute(query, id)

        # Return ingredients
        return cursor.fetchall()

    def get_count(self):
        '''Fetch the highest person id for a given user. This is used to
        genereate a index for a person.
        '''
        user_id = 1

        query = '''SELECT MAX(id) AS count
                     FROM person
                    WHERE user_id = %s'''

        cursor = connection.cursor()
        cursor.execute(query, user_id)

        # Return persons
        return cursor.fetchall()

    def get_persons(self):
        '''Fetch a list of all persons.'''
        user_id = 1

        query = '''SELECT *
                     FROM person
                    WHERE user_id = %s
                 ORDER BY name'''

        cursor = connection.cursor()
        cursor.execute(query, user_id)

        # Return persons
        return cursor.fetchall()
