class PersonModel:
    '''Model for the person pages. This model will handle all ineractions
    with the database.
    '''
    def add_person(self, ingredient):
        pass

    def edit_person(self, ingredient):
        pass

    def delete_person(self, index):
        pass

    def get_person(self, index):
        pass

    def get_persons(self):
        user_id = 1

        query = '''SELECT *
                     FROM person
                    WHERE account_id = %s'''

        cursor = connection.cursor()
        cursor.execute(query, user_id)

        persons = cursor.fetchall()

        return persons
