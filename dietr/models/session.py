from .. import connection

class SessionModel:
    '''Model for the authentication pages. This model will handle all
    ineractions with the database and cryptography.
    '''
    def generate_hash(self):
        pass

    def generate_salt(self):
        pass

    def get_hash(self, password, salt):
        pass

    def add_user(self, user):
        pass

    def get_user(self, username):
        query = '''SELECT *
                     FROM user
                    WHERE úsername = %s'''

        cursor = connection.cursor()
        cursor.execute(query, (username,))

        user = cursor.fetchone()

        return user

    def does_user_exist(self, email, username):
        query = '''SELECT (
                          SELECT COUNT(email)
                            FROM users
                           WHERE email = %s
                          ) AS email, (
                          SELECT COUNT(username)
                            FROM users
                           WHERE username = %s
                          ) AS username'''

        cursor = connection.cursor()
        cursor.execute(query, (email, username))

        return cursor.fetchone()
