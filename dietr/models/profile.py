from passlib.hash import pbkdf2_sha256

from .. import app, connection
from . import AuthenticationModel

class ProfileModel(AuthenticationModel):
    '''Model for the profile page. This model will handle all
    ineractions with the database and cryptography.
    '''
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
