from passlib.hash import pbkdf2_sha256

from .. import app, connection


class ProfileModel:
    '''Model for the profile page. This model will handle all
    ineractions with the database and cryptography.
    '''
    def generate_hash(self, password, salt=None):
        return pbkdf2_sha256.hash(password)

    def verify_hash(self, password, hash, salt=None):
        return pbkdf2_sha256.verify(password, hash)

    def get_user(self, id):
        query = '''SELECT *
                     FROM account
                    WHERE id = %s'''

        cursor = connection.cursor()
        cursor.execute(query, id)

        # Return user
        return cursor.fetchone()

    def update_user_with_password(self, user):
        query = '''UPDATE account
                      SET name = %s, username = %s, hash = %s, email = %s
                    WHERE id = %s'''

        cursor = connection.cursor()
        cursor.execute(query, (user['name'], user['username'], user['hash'],
                               user['email'], user['id']))

        # Execute query
        return connection.commit()

    def update_user_without_password(self, user):
        query = '''UPDATE account
                      SET name = %s, username = %s, email = %s
                    WHERE id = %s'''

        cursor = connection.cursor()
        cursor.execute(query, (user['name'], user['username'], user['email'],
                               user['id']))

        # Execute query
        return connection.commit()

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
