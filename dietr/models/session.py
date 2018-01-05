from passlib.hash import pbkdf2_sha256

from .. import connection

class SessionModel:
    '''Model for the authentication pages. This model will handle all
    ineractions with the database and cryptography.
    '''
    def generate_hash(password, salt = None):
        return pbkdf2_sha256.hash(user['password'])

    def add_person(user):
        query = '''INSERT INTO person (account_id, name, url)
                        VALUES (%s, %s)'''

        cursor = connection.cursor()
        cursor.execute(query, (user['id'], user['name'], user['url']))

        # Execute query
        return connection.commit()

    def add_user(self, user):
        query = '''INSERT INTO account (name, username, hash, email)
                        VALUES (%s, %s, %s, %s, %s)'''

        cursor = connection.cursor()
        cursor.execute(query, (user['name'], user['username'], user['hash'],
                                                               user['email']))

        # Execute query
        return connection.commit()

    def get_user(self, username):
        query = '''SELECT *
                     FROM user
                    WHERE username = %s'''

        cursor = connection.cursor()
        cursor.execute(query, (username,))

        # Return user
        return cursor.fetchone()

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

        # Retrun number of matching mail adresses and usernames
        return cursor.fetchone()
