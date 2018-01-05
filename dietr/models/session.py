from .. import connection

class SessionModel:
    '''Model for the authentication pages. This model will handle all
    ineractions with the database and cryptography.
    '''

    def add_person(id, name):
        query="insert into person (account_id, name) values (%s, %s);"
        cursor=connection.cursor()
        cursor.execute(query, (id, name))
        return None

    def add_user(self, username, name, hash, email):
        query="insert into account (name, username, hash, email) values (%s, %s, %s, %s, %s);"
        cursor=connection.cursor()
        cursor.execute(query, (name, username, hash, email))
        userdata=cursor.fetchone()
        add_person(userdata[0], name)
        return None

    def get_user(self, username):
        query = '''SELECT *
                     FROM user
                    WHERE úsername = %s'''

        cursor = connection.cursor()
        cursor.execute(query, (username,))

        user = cursor.fetchone()

        return user

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

        return cursor.fetchone()
