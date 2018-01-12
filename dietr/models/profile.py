from dietr import database
from dietr.models.authentication import AuthenticationModel


class ProfileModel(AuthenticationModel):
    def set_password(self, id, password):
        hash = self.generate_hash(password)

        query = '''UPDATE users
                      SET hash = %s
                    WHERE id = %s;'''

        database.commit(query, (hash, id))

    def set_email(self, id, email):
        query = '''UPDATE users
                      SET email = %s
                    WHERE id = %s;'''

        database.commit(query, (mail, id))

    def set_username(self, id, username):
        query = '''UPDATE users
                      SET username = %s
                    WHERE id = %s;'''

        database.commit(query, (handle, id))

    def set_name(self, id, first_name, middle_name, last_name):
        query = '''UPDATE users
                      SET first_name = %s,
                          middle_name = %s,
                          last_name = %s
                    WHERE id = %s;'''

        database.commit(query, (first_name, middle_name, last_name, id))
