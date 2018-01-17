import pymysql as sql

from dietr.utils import singleton


@singleton
class Database:
    def __init__(self):
        self.connection = None

    def close(self):
        self.connection.close()

    def connect(self):
        self.connection = sql.connect(database='renswnc266_development',
                                      host='185.182.57.56',
                                      user='renswnc266_dietr',
                                      password='qvuemzxu',
                                      cursorclass=sql.cursors.DictCursor)

    def commit(self, query, arugments=()):
        with self.connection.cursor() as cursor:
            cursor.execute(query, arugments)

            self.connection.commit()

    def fetch(self, query, arugments=()):
        with self.connection.cursor() as cursor:
            cursor.execute(query, arugments)

            return cursor.fetchone()

    def fetch_all(self, query, arugments=()):
        with self.connection.cursor() as cursor:
            cursor.execute(query, arugments)

            return cursor.fetchall()


database = Database()
