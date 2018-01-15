from passlib.hash import sha256_crypt as sha256

from dietr.database import database
from dietr.models.user import User


class AuthenticationModel:
    def generate_hash(self, password):
        """Generate a sha256 hash of a password."""
        return sha256.hash(password)

    def verify_password(self, password, hash):
        """Check if the password matches the hash. Returns a boolean."""
        return sha256.verify(password, hash)

    def add_user(self, username, email, first_name, middle_name, last_name,
                 password):
        """Add a user to the database."""
        hash = self.generate_hash(password)

        query = '''INSERT INTO users (username, email, first_name, middle_name,
                                      last_name, hash)
                        VALUES (%s, %s, %s, %s, %s, %s)'''

        database.commit(query, (username, email, first_name, middle_name,
                                last_name, hash))

    def get_user(self, username):
        """Get a user from the database."""
        query = '''SELECT id, username, email, first_name, middle_name,
                          last_name, hash
                     FROM users
                    WHERE username = %s'''

        # Convert dict to an user object
        return User(**database.fetch(query, username))

    def does_user_exist(self, username, email):
        """Get the number of users with a username and email from the database.
        """
        query = '''SELECT (SELECT COUNT(username)
                             FROM users
                            WHERE username = %s) AS username_count,
                          (SELECT COUNT(email)
                             FROM users
                            WHERE email = %s) AS email_count'''

        # Retrun number of matching usernames and mail adresses
        return database.fetch(query, (username, email))
