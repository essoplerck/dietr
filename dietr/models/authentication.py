from dataclasses import dataclass, field

from passlib.hash import sha256_crypt as sha256

from dietr import database


@dataclass
class User:
    id: int
    username: str
    email: str
    first_name: str
    middle_name: str
    last_name: str
    hash: str
    allergies: list = field(default_factory=list, init=False)
    ingredients: list = field(default_factory=list, init=False)

    @property
    def name(self):
        if self.middle_name:
            return f'{self.first_name} {self.middle_name} {self.last_name}'

        else:
            return f'{self.first_name} {self.last_name}'


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

    def get_user_by_id(self, id):
        query = '''SELECT username, email, first_name, middle_name, last_name, hash
                     FROM users
                    WHERE id = %s'''

        (username, email, first_name, middle_name, last_name, hash) = database.fetch(query, id)

        return User(id, username, email, first_name, middle_name, last_name, hash)

    def does_user_exist(self, username, email):
        query = '''SELECT (SELECT COUNT(username)
                             FROM users
                            WHERE username = %s) AS username_count,
                          (SELECT COUNT(email)
                             FROM users
                            WHERE email = %s) AS email_count'''

        # Retrun number of matching usernames and mail adresses
        return database.fetch(query, (username, email))
