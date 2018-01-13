from dataclasses import dataclass, field

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
    preferences: list = field(default_factory=list, init=False)

    @property
    def name(self):
        if self.middle_name:
            return f'{self.first_name} {self.middle_name} {self.last_name}'

        else:
            return f'{self.first_name} {self.last_name}'


class UserModel:
    def get_user(self, id):
        query = '''SELECT username,
                          email,
                          first_name, middle_name, last_name,
                          hash
                     FROM users
                    WHERE id = %s'''

        (username, email, first_name, middle_name, last_name, hash) = database.fetch(query, id)

        return User(id, username, email, first_name, middle_name, last_name, hash)
