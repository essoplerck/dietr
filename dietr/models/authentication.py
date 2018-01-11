from dataclasses import dataclass, field

from passlib.hash import sha256_crypt

from dietr import database


@dataclass
class User:
    id: int
    handle: str
    mail: str
    first_name: str
    middle_name: str
    last_name: str
    hash: str
    salt: str
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
    def generate_salt(self):
        return 'salt'

    def generate_hash(self, password, salt):
        return 'hash'

    def verify_password(self, password, hash, salt):
        return True

    def add_user(self, handle, mail, first_name, middle_name, last_name, password):
        salt = self.generate_salt()
        hash = self.generate_hash(password, salt)

        query = '''INSERT INTO users (handle, mail, first_name, middle_name, last_name, hash, salt)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)'''

        print(handle, mail, first_name, middle_name, last_name, hash, salt)

        database.commit(query, (handle, mail, first_name, middle_name, last_name, hash, salt))

    def get_user(self, handle):
        query = '''SELECT id, mail, first_name, middle_name, last_name, hash, salt
                     FROM users
                    WHERE handle = %s'''

        (handle, mail, first_name, middle_name, last_name, hash, salt) = database.fetch(query, handle)

        return User(id, handle, mail, first_name, middle_name, last_name, hash, salt)

    def get_user_by_id(self, id):
        query = '''SELECT handle, mail, first_name, middle_name, last_name, hash, salt
                     FROM users
                    WHERE id = %s'''

        (handle, mail, first_name, middle_name, last_name, hash, salt) = database.fetch(query, id)

        return User(id, handle, mail, first_name, middle_name, last_name, hash, salt)

    def does_user_exist(self, handle, mail):
        query = '''SELECT (SELECT COUNT(handle)
                             FROM users
                            WHERE handle = %s) AS handle_count,
                          (SELECT COUNT(mail)
                             FROM users
                            WHERE mail = %s) AS mail_count'''

        # Retrun number of matching usernames and mail adresses
        return database.fetch(query, (handle, mail))
