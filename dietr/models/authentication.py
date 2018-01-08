from passlib.hash import pbkdf2_sha256

from .. import app, connection


class AuthenticationModel:
    '''Model for the authentication pages. This model will handle all
    ineractions with the database and cryptography.
    '''
    def generate_hash(self, password, salt = None):
        return pbkdf2_sha256.hash(password)


    def verify_hash(self, password, hash, salt = None):
        return pbkdf2_sha256.verify(password, hash)


    def add_user(self, user):
        query = '''INSERT INTO account (name, username, hash, email)
                        VALUES (%s, %s, %s, %s)'''

        cursor = connection.cursor()
        cursor.execute(query, (user['name'], user['username'], user['hash'],
                                                               user['email']))

        # Execute query
        return connection.commit()


    def get_user(self, username):
        query = '''SELECT *
                     FROM account
                    WHERE username = %s'''

        cursor = connection.cursor()
        cursor.execute(query, (username,))

        # Return user
        return cursor.fetchone()


    def does_user_exist(self, email, username):
        query = '''SELECT (
                          SELECT COUNT(email)
                            FROM account
                           WHERE email = %s
                          ) AS email, (
                          SELECT COUNT(username)
                            FROM account
                           WHERE username = %s
                          ) AS username'''

        cursor = connection.cursor()
        cursor.execute(query, (email, username))

        # Retrun number of matching mail adresses and usernames
        return cursor.fetchone()
