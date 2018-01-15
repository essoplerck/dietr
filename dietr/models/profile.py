from dietr.database import database
from dietr.models.authentication import AuthenticationModel


class ProfileModel(AuthenticationModel):
    def set_password(self, id, password):
        """Set the user password."""
        hash = self.generate_hash(password)

        query = '''UPDATE users
                      SET hash = %s
                    WHERE id = %s;'''

        database.commit(query, (hash, id))

    def set_email(self, id, email):
        """Set the email adress of the user."""
        query = '''UPDATE users
                      SET email = %s
                    WHERE id = %s;'''

        database.commit(query, (mail, id))

    def set_username(self, id, username):
        """Set the username of the user."""
        query = '''UPDATE users
                      SET username = %s
                    WHERE id = %s;'''

        database.commit(query, (handle, id))

    def set_name(self, id, first_name, middle_name, last_name):
        """Set  the name of the user."""
        query = '''UPDATE users
                      SET first_name = %s,
                          middle_name = %s,
                          last_name = %s
                    WHERE id = %s;'''

        database.commit(query, (first_name, middle_name, last_name, id))
