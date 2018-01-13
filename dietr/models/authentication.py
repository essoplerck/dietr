from passlib.hash import sha256_crypt as sha256

from dietr import database
from dietr.models.user import User


class AuthenticationModel:
    '''Model for the authentication pages. This model will handle all
    ineractions with the database and cryptography.
    '''
    def generate_hash(self, password):
        return sha256.hash(password)

    def verify_password(self, password, hash):
        return sha256.verify(password, hash)

    def add_user(self, username, email, first_name, middle_name, last_name, password):
        hash = self.generate_hash(password)

        query = '''INSERT INTO users (username, email, first_name, middle_name, last_name, hash)
                        VALUES (%s, %s, %s, %s, %s, %s)'''

        database.commit(query, (username, email, first_name, middle_name, last_name, hash))

    def get_user(self, username):
        query = '''SELECT id, email, first_name, middle_name, last_name, hash
                     FROM users
                    WHERE username = %s'''

        (id, email, first_name, middle_name, last_name, hash) = database.fetch(query, username)

        return User(id, username, email, first_name, middle_name, last_name, hash)

    def does_user_exist(self, username, email):
        query = '''SELECT (SELECT COUNT(username)
                             FROM users
                            WHERE username = %s) AS username_count,
                          (SELECT COUNT(email)
                             FROM users
                            WHERE email = %s) AS email_count'''

        # Retrun number of matching usernames and mail adresses
        return database.fetch(query, (username, email))[0]
